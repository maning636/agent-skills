#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
agent-skills 取用工具（零依赖，仅标准库）

用法:
  python fetch.py <domain>/<skill>            # 取单个技能，命中缓存不发请求；打印正文
  python fetch.py --fetch <domain>/<skill>     # 同上（位置参数与 --fetch 等价）
  python fetch.py --path <domain>/<skill>      # 同上，但只打印本地路径
  python fetch.py --index                      # 取 L0 索引（领域路由表，唯一该常驻的文件）
  python fetch.py --l1 <domain>                # 取某领域的 L1 索引（该领域技能清单）
  python fetch.py --raw <仓库内相对路径>        # 取任意文件（如某技能的 references/xxx.md）
  python fetch.py --ls <仓库内目录>             # 列出目录内容（用于发现技能的附属文件）
  python fetch.py --search "招聘 面试"          # 在 L0+L1 中搜索，返回候选（带直链）
  python fetch.py --search "面试" --domain human-resources
  python fetch.py --cache-dir                  # 打印缓存目录
  python fetch.py --cache-clear                # 一键清理本地缓存
  python fetch.py --cache-clear-dry-run        # 预览将要清理的缓存
  python fetch.py --composition one-person-company   # 解析 skills-meta 的 composition
  python fetch.py --pin-list                   # 列出已固定的库版本（库@tag）
  python fetch.py --update                     # 强制重新拉取（忽略缓存）
  python fetch.py --offline <domain>/<skill>   # 只用缓存，不联网

设计原则:
  * 绝不整包下载；一次只取需要的文件
  * 网络失败自动降级到本地缓存
  * 取不到就报错退出，绝不返回编造内容
  * composition 解析只打印「库@tag + 技能 id」，不代跑，避免误拉
"""
import argparse, json, os, re, shutil, sys, time, urllib.request

RAW_BASE = "https://raw.githubusercontent.com/maning636/agent-skills/main/"
# raw 主站失败时的备用通道（同一份内容）
ALT_BASE = "https://github.com/maning636/agent-skills/raw/main/"
# 目录列举用 GitHub tree API（一次拿全仓文件树，之后走缓存）
TREE_URL = "https://api.github.com/repos/maning636/agent-skills/git/trees/main?recursive=1"
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "agent-skills")
# 缓存有效期（秒）。
# L0 是路由表：变一次整个检索都受影响，所以 1 小时自动刷新（只有几 KB）。
# L1 是各域清单：新增域时旧缓存里根本没有该域，所以也要自动刷新（32 个共约 120 KB）。
# L2 技能正文体积大且稳定，默认永久缓存，需要时用 --update 手动刷新。
L0_TTL = 3600
L1_TTL = 21600


def _is_index(rel):
    return rel == "INDEX.md" or (rel.startswith("domains/") and rel.endswith("/INDEX.md"))

try:  # Windows 控制台默认 GBK，强制 UTF-8 输出避免中文乱码
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ----------------------------------------------------------------- 网络
def _get(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": "agent-skills-fetch/1.0 (+https://github.com/maning636/agent-skills)",
        "Accept": "text/plain, */*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _get_retry(rel, tries=3):
    """依次尝试 raw 主站 / 备用通道 / 重试。返回 bytes。全部失败抛最后一个异常。"""
    err = None
    for base in (RAW_BASE, ALT_BASE):
        url = base + rel
        for i in range(tries if base == RAW_BASE else 1):
            try:
                return _get(url)
            except Exception as e:
                err = e
                if i + 1 < tries:
                    time.sleep(0.6 * (i + 1))
    raise err


def cache_path(rel):
    return os.path.join(CACHE, "latest", *rel.replace("\\", "/").lstrip("/").split("/"))


def fetch(rel, offline=False, force=False, ttl=0):
    """取仓库内相对路径内容。返回 (text, from_cache)。取不到抛异常。

    ttl>0 时，缓存文件超过该秒数就重新拉取（用于 L0 这种入口索引，
    它一变整个路由表就失效，代价只有几 KB）。
    """
    rel = rel.replace("\\", "/").lstrip("/")
    local = cache_path(rel)
    fresh = os.path.isfile(local) and (ttl <= 0 or (time.time() - os.path.getmtime(local)) < ttl)
    if fresh and not force:
        return open(local, encoding="utf-8", errors="replace").read(), True
    if offline:
        if os.path.isfile(local):
            return open(local, encoding="utf-8", errors="replace").read(), True
        raise FileNotFoundError("离线且无缓存: %s" % rel)
    url = RAW_BASE + rel
    try:
        data = _get_retry(rel)
    except Exception as e:
        if os.path.isfile(local):
            return open(local, encoding="utf-8", errors="replace").read(), True
        raise RuntimeError("拉取失败 %s (%s: %s)；本地缓存也没有: %s"
                           % (url, type(e).__name__, e, local))
    os.makedirs(os.path.dirname(local), exist_ok=True)
    with open(local, "wb") as f:
        f.write(data)
    with open(local + ".source", "w", encoding="utf-8") as f:
        f.write(url + "\n")
    return data.decode("utf-8", errors="replace"), False


# ----------------------------------------------------------------- 解析
def parse_domains(l0):
    """L0 表格 → [(domain, 中文名, 触发词, 技能数)]"""
    out = []
    for line in l0.splitlines():
        m = re.match(r"^\|\s*\d+\s*\|\s*\*\*(.+?)\*\*\s*`([a-z0-9\-]+)`\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|", line)
        if m:
            out.append((m.group(2), m.group(1), m.group(3), int(m.group(4))))
    return out


def parse_skills(l1):
    """L1 表格 → [(name, 中文标签, 关键词, 路径, 大小)]"""
    out = []
    for line in l1.splitlines():
        m = re.match(r"^\|\s*`([^`]+)`\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*`([^`]+)`\s*\|\s*([\d.]+[KM])\s*\|", line)
        if m:
            out.append((m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)))
    return out


# ----------------------------------------------------------------- 打分
CJK = re.compile(r"[\u4e00-\u9fff]")


def tokenize(q):
    """中文：整词 + 二元组；英文：小写词"""
    toks, grams = [], []
    for part in re.split(r"[\s,，、;；/\\|+]+", q or ""):
        if not part:
            continue
        if CJK.search(part):
            toks.append(part.lower())
            runs = re.findall(r"[\u4e00-\u9fff]+", part)
            for run in runs:
                for i in range(len(run) - 1):
                    grams.append(run[i:i + 2])
        else:
            toks.extend(w.lower() for w in re.findall(r"[A-Za-z0-9_\-]+", part))
    return toks, grams


def score(text, toks, grams):
    t = text.lower()
    s = 0
    for tok in toks:
        if tok in t:
            s += 6 if len(tok) >= 3 else 3
    for g in grams:
        if g in t:
            s += 2
    return s


def score_tokens(text, toks):
    """只按整词计分，不看二元组。

    领域路由必须用这个：像「人力资源」这种域名里偶然含有「资源」，
    会被查询「我的资源有哪些」的二元组误命中，再乘 3 倍域权重就压过了
    真正命中的技能。整词命中才是「触发词里确实有这个词」的可靠信号。
    """
    t = text.lower()
    s = 0
    for tok in toks:
        if tok in t:
            s += 6 if len(tok) >= 3 else 3
    return s


# ----------------------------------------------------------------- 元库（skills-meta）
def meta_root():
    """定位 skills-meta 元库根目录。

    优先级: $SKILLS_META 环境变量 -> D:\\skills-meta -> ~/skills-meta
    """
    env = os.environ.get("SKILLS_META")
    cands = [env] if env else []
    cands += [r"D:\skills-meta", os.path.join(os.path.expanduser("~"), "skills-meta")]
    for c in cands:
        if c and os.path.isdir(c):
            return os.path.abspath(c)
    return None


def _read_pin(meta):
    """读 pin 文件: <lib>@<tag> 每行一条，# 开头为注释。"""
    pins = {}
    p = os.path.join(meta, "pin")
    if not os.path.isfile(p):
        return pins
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for sep in ("@", "="):
            if sep in line:
                k, _, v = line.partition(sep)
                pins[k.strip()] = v.strip()
                break
    return pins


def _read_yaml(path):
    """极简 YAML 读取（只支持本项目用到的两层结构），无 PyYAML 依赖。"""
    try:
        import yaml  # 有就用标准库之外最稳的
        with open(path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except Exception:
        pass
    # 回退：手写解析 include: / - library: / domains: / skills:
    out, cur = {}, None
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError:
        return out
    section = None
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("include:"):
            section = "include"
            out.setdefault("include", [])
            continue
        if s.startswith("name:"):
            out["name"] = s.split(":", 1)[1].strip()
            continue
        if s.startswith("- ") and section == "include":
            item = {}
            rest = s[2:].strip()
            if ":" in rest:
                k, _, v = rest.partition(":")
                item[k.strip()] = v.strip()
            out["include"].append(item)
            cur = item
            continue
        if cur is not None and ":" in s:
            k, _, v = s.partition(":")
            cur[k.strip()] = v.strip()
    return out


def do_pin_list():
    meta = meta_root()
    if not meta:
        print("找不到 skills-meta 元库。设置 $SKILLS_META 或放到 D:\\skills-meta。", file=sys.stderr)
        return 1
    pins = _read_pin(meta)
    if not pins:
        print("pin 文件为空或不存在: %s" % os.path.join(meta, "pin"))
        return 1
    print("# 已固定的库版本 (skills-meta/pin)\n")
    for k in sorted(pins):
        print("  %-28s @ %s" % (k, pins[k]))
    return 0


def do_composition(name, offline=False, force=False):
    """解析 composition，输出「库@tag + 技能 id 列表」，并给出一条可复制的取用命令。"""
    meta = meta_root()
    if not meta:
        print("找不到 skills-meta 元库。设置 $SKILLS_META 或放到 D:\\skills-meta。", file=sys.stderr)
        return 1
    cpath = os.path.join(meta, "compositions", "%s.yaml" % name)
    if not os.path.isfile(cpath):
        print("未知 composition: %s（可选: %s）"
              % (name, ", ".join(sorted(
                  f[:-5] for f in os.listdir(os.path.join(meta, "compositions"))
                  if f.endswith(".yaml")))), file=sys.stderr)
        return 1
    comp = _read_yaml(cpath)
    pins = _read_pin(meta)
    includes = comp.get("include") or []

    print("本次使用：composition=%s" % name)
    if comp.get("description"):
        print("  说明: %s" % comp["description"])
    print()

    total = 0
    lines = []
    for inc in includes:
        lib = inc.get("library", "")
        base, _, want_tag = lib.partition("@")
        tag = want_tag or pins.get(base, "")
        doms = inc.get("domains", "")
        sks = inc.get("skills", "")
        if not tag:
            print("  ! %s 未固定版本（pin 里没有），按 main 处理" % base)
            tag = "main"
        if base.startswith("plugin:"):
            print("  库 %s@%s   [插件，优先于我们的技能]" % (base, tag))
        else:
            print("  库 %s@%s" % (base, tag))
        if doms:
            print("      domains: %s" % doms)
        if sks:
            print("      skills : %s" % sks)
        n = len([x for x in re.split(r"[,\s]+", str(doms or "")) if x])
        n += len([x for x in re.split(r"[,\s]+", str(sks or "")) if x])
        total += n
        lines.append("    %s@%s" % (base, tag))
    print()
    print("  技能 id 数量（按组成项计）: %d" % total)
    print("  取用:")
    for l in lines:
        print("    # %s" % l)
    print("    python tools/fetch.py --index      # 再按 L0 路由表逐个取")
    print()
    print("  提示: 插件优先 —— 通用工艺（脑暴/计划/TDD/调试/评审/并行/验证）先查插件；")
    print("        商业判断/OPC/设计令牌/企业运营/指标口径 只从本库与 opc-playbook 取。")
    return 0


def do_cache_clear(dry_run=False):
    """一键清理本地缓存。"""
    if not os.path.isdir(CACHE):
        print("缓存目录不存在，无需清理: %s" % CACHE)
        return 0
    n = sum(len(files) for _, _, files in os.walk(CACHE))
    size = sum(os.path.getsize(os.path.join(r, f))
               for r, _, fs in os.walk(CACHE) for f in fs
               if os.path.exists(os.path.join(r, f)))
    if dry_run:
        print("将清理: %s（%d 个文件 / %.1f MB）" % (CACHE, n, size / 1048576))
        return 0
    shutil.rmtree(CACHE, ignore_errors=True)
    print("已清理缓存: %s（%d 个文件 / %.1f MB）" % (CACHE, n, size / 1048576))
    return 0


# ----------------------------------------------------------------- 动作
def _tree(offline=False, force=False):
    """取全仓文件树（GitHub tree API），本地缓存一次即可复用。

    只缓存用得到的字段（path/type/size），原始响应约 1.5 MB，精简后约 250 KB。
    """
    p = os.path.join(CACHE, "_tree.json")
    if os.path.isfile(p) and not force:
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            pass
    if offline:
        raise FileNotFoundError("离线且无文件树缓存: %s" % p)
    req = urllib.request.Request(TREE_URL, headers={
        "User-Agent": "agent-skills-fetch/1.0 (+https://github.com/maning636/agent-skills)",
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(req, timeout=40) as r:
        raw = json.loads(r.read().decode("utf-8"))
    slim = {
        "truncated": bool(raw.get("truncated")),
        "tree": [{"path": it.get("path", ""), "type": it.get("type", ""),
                  "size": it.get("size", 0)} for it in raw.get("tree", [])],
    }
    os.makedirs(CACHE, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(slim, f, separators=(",", ":"))
    return slim


def do_ls(dirpath, offline=False, force=False):
    """列出仓库内某目录的内容（按目录分组），用于发现技能的 references/ assets/ 等附属文件。"""
    d = (dirpath or "").replace("\\", "/").strip("/")
    try:
        data = _tree(offline=offline, force=force)
    except Exception as e:
        print("错误: %s" % e, file=sys.stderr)
        return 1
    if data.get("truncated"):
        print("注意: 文件树被 GitHub 截断，列表可能不完整", file=sys.stderr)
    pref = (d + "/") if d else ""
    files, dirs = [], set()
    for it in data.get("tree", []):
        p = it.get("path", "")
        if not p.startswith(pref):
            continue
        rel = p[len(pref):]
        if not rel:
            continue
        if "/" in rel:
            dirs.add(rel.split("/", 1)[0] + "/")   # 只显示第一层子目录
        elif it.get("type") == "tree":
            dirs.add(rel + "/")
        else:
            files.append((rel, it.get("size", 0)))
    if not files and not dirs:
        print("空目录或不存在: %s" % (d or "/"), file=sys.stderr)
        return 1
    print("# 目录内容: %s" % (d or "/"))
    for name in sorted(dirs):
        print("  %-46s %8s" % (name, "<dir>"))
    for rel, size in sorted(files):
        print("  %-46s %8s" % (rel, "%dB" % size))
    print("\n取用: python fetch.py --raw <路径>")
    if dirs:
        print("进子目录: python fetch.py --ls %s%s" % (pref, sorted(dirs)[0]))
    return 0


def do_raw(rel, offline=False, force=False, path_only=False):
    """取仓库内任意相对路径（L0 / L1 / 附属文件都走这里）。"""
    rel = (rel or "").replace("\\", "/").strip("/")
    if not rel:
        print("用法: fetch.py --raw <仓库内相对路径>", file=sys.stderr)
        return 2
    try:
        txt, cached = fetch(rel, offline=offline, force=force,
                            ttl=(L0_TTL if rel == "INDEX.md" else
                                 L1_TTL if _is_index(rel) else 0))
    except Exception as e:
        print("错误: %s" % e, file=sys.stderr)
        print("提示：该文件不可用。如需它，请告知用户缺少哪个文件，不要凭印象编造内容。", file=sys.stderr)
        return 1
    if path_only:
        print(cache_path(rel))
        return 0
    if cached:
        print("<!-- from cache: %s -->" % cache_path(rel), file=sys.stderr)
    sys.stdout.write(txt)
    return 0


def do_search(query, domain=None, limit=12):
    toks, grams = tokenize(query)
    l0, _ = fetch("INDEX.md", ttl=L0_TTL)
    doms = parse_domains(l0)
    if domain:
        doms = [d for d in doms if d[0] == domain]
        if not doms:
            print("未知领域: %s（可选：%s）" % (domain, ", ".join(d[0] for d in parse_domains(l0))),
                  file=sys.stderr)
            return 2
    hits = []
    for dname, dzh, dtrig, dcount in doms:
        # 领域触发词是精修字段，整词命中才算数（不看二元组，避免误命中）
        ds = score_tokens(dzh + " " + dtrig, toks) * 2
        try:
            l1, _ = fetch("domains/%s/INDEX.md" % dname, ttl=L1_TTL)
        except Exception as e:
            print("跳过 %s: %s" % (dname, e), file=sys.stderr)
            continue
        for name, label, keys, path, size in parse_skills(l1):
            # 关键词列是人工精修的高精度字段，权重加倍；
            # 名称+标签次之（名称本身多含英文，容易被噪音词命中）
            ss = score(keys, toks, grams) * 2 + score(name + " " + label, toks, grams)
            if name.lower() in [t for t in toks]:
                ss += 12
            hits.append((ss + ds * 3, dname, name, label, keys, path, size))
    hits.sort(reverse=True)
    hits = [h for h in hits if h[0] > 0]
    if not hits:
        print("没有匹配项。先读 L0: %sINDEX.md" % RAW_BASE)
        return 1
    print("# 候选技能（query=%r）\n" % query)
    for s, dname, name, label, keys, path, size in hits[:limit]:
        print("  [%s/%s]  %s   %s" % (dname, name, label, size))
        print("      %s" % keys[:140])
        print("      %s%s" % (RAW_BASE, path))
    print("\n取用: python fetch.py <domain>/<skill>")
    return 0


def do_fetch(spec, offline=False, force=False, path_only=False):
    if "/" not in spec:
        print("用法: fetch.py <domain>/<skill>", file=sys.stderr)
        return 2
    domain, skill = spec.split("/", 1)
    rel = "domains/%s/%s/SKILL.md" % (domain, skill)
    try:
        txt, cached = fetch(rel, offline=offline, force=force)
    except Exception as e:
        print("错误: %s" % e, file=sys.stderr)
        print("提示：该技能不可用。如需它，请告知用户缺少哪个技能，不要凭印象编造流程。", file=sys.stderr)
        return 1
    if path_only:
        print(cache_path(rel))
        return 0
    if cached:
        print("<!-- from cache: %s -->" % cache_path(rel), file=sys.stderr)
    sys.stdout.write(txt)
    return 0


def main():
    ap = argparse.ArgumentParser(description="agent-skills 按需取用")
    ap.add_argument("spec", nargs="?", help="domain/skill")
    ap.add_argument("--fetch", dest="fetch_spec", help="domain/skill（与位置参数等价）")
    ap.add_argument("--search", help="搜索关键词")
    ap.add_argument("--domain", help="限定领域")
    ap.add_argument("--index", "--l0", dest="index", action="store_true",
                    help="取 L0 索引（领域路由表）")
    ap.add_argument("--l1", metavar="DOMAIN", help="取某领域的 L1 索引")
    ap.add_argument("--raw", metavar="PATH", help="取仓库内任意相对路径")
    ap.add_argument("--ls", metavar="DIR", help="列出仓库内某目录内容")
    ap.add_argument("--path", action="store_true", help="只打印本地路径")
    ap.add_argument("--cache-dir", action="store_true", help="打印缓存目录")
    ap.add_argument("--cache-clear", action="store_true", help="一键清理本地缓存")
    ap.add_argument("--cache-clear-dry-run", action="store_true", help="预览将要清理的缓存")
    ap.add_argument("--composition", metavar="NAME", help="解析 skills-meta 里的 composition")
    ap.add_argument("--pin-list", action="store_true", help="列出已固定的库版本")
    ap.add_argument("--update", action="store_true", help="强制重新拉取")
    ap.add_argument("--offline", action="store_true", help="只用缓存，不联网")
    a = ap.parse_args()

    if a.cache_clear:
        return do_cache_clear()
    if a.cache_clear_dry_run:
        return do_cache_clear(dry_run=True)
    if a.pin_list:
        return do_pin_list()
    if a.composition:
        return do_composition(a.composition, offline=a.offline, force=a.update)
    if a.cache_dir:
        print(CACHE)
        return 0
    if a.search:
        return do_search(a.search, a.domain)
    if a.index:
        return do_raw("INDEX.md", offline=a.offline, force=a.update, path_only=a.path)
    if a.l1:
        return do_raw("domains/%s/INDEX.md" % a.l1, offline=a.offline, force=a.update, path_only=a.path)
    if a.raw:
        return do_raw(a.raw, offline=a.offline, force=a.update, path_only=a.path)
    if a.ls is not None:
        return do_ls(a.ls, offline=a.offline, force=a.update)
    spec = a.fetch_spec or a.spec
    if spec:
        return do_fetch(spec, a.offline, a.update, a.path)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
