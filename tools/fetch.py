#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
agent-skills 取用工具（零依赖，仅标准库）

用法:
  python fetch.py <domain>/<skill>            # 取单个技能，命中缓存不发请求；打印正文
  python fetch.py --fetch <domain>/<skill>     # 同上（位置参数与 --fetch 等价）
  python fetch.py --path <domain>/<skill>      # 同上，但只打印本地路径
  python fetch.py --search "招聘 面试"          # 在 L0+L1 中搜索，返回候选（带直链）
  python fetch.py --search "面试" --domain human-resources
  python fetch.py --cache-dir                  # 打印缓存目录
  python fetch.py --update                     # 强制重新拉取（忽略缓存）
  python fetch.py --offline <domain>/<skill>   # 只用缓存，不联网

设计原则:
  * 绝不整包下载；一次只取需要的文件
  * 网络失败自动降级到本地缓存
  * 取不到就报错退出，绝不返回编造内容
"""
import argparse, os, re, sys, time, urllib.request

RAW_BASE = "https://raw.githubusercontent.com/maning636/agent-skills/main/"
# raw 主站失败时的备用通道（同一份内容）
ALT_BASE = "https://github.com/maning636/agent-skills/raw/main/"
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "agent-skills")

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


def fetch(rel, offline=False, force=False):
    """取仓库内相对路径内容。返回 (text, from_cache)。取不到抛异常。"""
    rel = rel.replace("\\", "/").lstrip("/")
    local = cache_path(rel)
    if os.path.isfile(local) and not force:
        return open(local, encoding="utf-8", errors="replace").read(), True
    if offline:
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


# ----------------------------------------------------------------- 动作
def do_search(query, domain=None, limit=12):
    toks, grams = tokenize(query)
    l0, _ = fetch("INDEX.md")
    doms = parse_domains(l0)
    if domain:
        doms = [d for d in doms if d[0] == domain]
        if not doms:
            print("未知领域: %s（可选：%s）" % (domain, ", ".join(d[0] for d in parse_domains(l0))),
                  file=sys.stderr)
            return 2
    hits = []
    for dname, dzh, dtrig, dcount in doms:
        ds = score(dzh + " " + dtrig, toks, grams)
        try:
            l1, _ = fetch("domains/%s/INDEX.md" % dname)
        except Exception as e:
            print("跳过 %s: %s" % (dname, e), file=sys.stderr)
            continue
        for name, label, keys, path, size in parse_skills(l1):
            ss = score(name + " " + label + " " + keys, toks, grams)
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
    ap.add_argument("--path", action="store_true", help="只打印本地路径")
    ap.add_argument("--cache-dir", action="store_true", help="打印缓存目录")
    ap.add_argument("--update", action="store_true", help="强制重新拉取")
    ap.add_argument("--offline", action="store_true", help="只用缓存，不联网")
    a = ap.parse_args()

    if a.cache_dir:
        print(CACHE)
        return 0
    if a.search:
        return do_search(a.search, a.domain)
    spec = a.fetch_spec or a.spec
    if spec:
        return do_fetch(spec, a.offline, a.update, a.path)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
