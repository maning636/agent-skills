#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成 tools/zh_keys.py —— 每个技能的「中文标签 + 中文关键词」。

优先级：
  1. curated_zh.ZH       —— 手工维护，质量最高
  2. curated_zh.ZH_NEW   —— 手工维护的新批次
  3. 自动抽取            —— 从 description 的「触发词：」或中文短语里抽

用法：  python tools/gen_zh_keys.py [--check]
"""
import os, re, sys, io, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

import curated_zh  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('--check', action='store_true', help='只检查覆盖率，不写文件')
A = ap.parse_args()

NOISE = {'工具', '技能', '当用户', '使用', '支持', '提供', '通过', '需要', '可以',
         '仅在', '本工具', '不负责', '适用于', '该工具', '一个', '进行', '用于',
         '这是', '如果', '或者', '可以', '文件', '内容', '结果', '本身', '默认',
         '用户', '时候', '场景', '触发', '以下', '如下', '包含', '包括', '等等',
         '所有', '其他', '以及', '或者', '需要', '必须', '不得', '不会', '不能'}
EN_STOP = {'the', 'and', 'for', 'with', 'that', 'this', 'from', 'are', 'was', 'you',
           'not', 'can', 'all', 'any', 'its', 'has', 'use', 'via', 'tool', 'skill',
           'cli', 'run', 'make', 'your', 'how', 'what', 'when', 'into', 'out'}


def get_desc(p):
    t = open(p, encoding='utf-8', errors='replace').read()
    if not t.startswith('---'):
        return '', ''
    parts = t.split('---', 2)
    fm = parts[1]
    body = parts[2] if len(parts) > 2 else ''
    m = re.search(r'^description:\s*(.*)$', fm, re.M)
    if not m:
        return '', body
    if m.group(1).strip() in ('>-', '>', '|', '|-', '>+'):
        lines = fm.splitlines()
        i = lines.index(m.group(0))
        buf, j = [], i + 1
        while j < len(lines) and not re.match(r'^[A-Za-z_][A-Za-z0-9_-]*:', lines[j]):
            buf.append(lines[j].strip()); j += 1
        return ' '.join(x for x in buf if x), body
    v = m.group(1).strip()
    if len(v) > 1 and v[0] == v[-1] and v[0] in '"\'':
        v = v[1:-1]
    return v, body


def _push(kw, term):
    term = term.strip(" 。.\"'，,、（）()【】[]")
    if not term or len(term) > 14:
        return
    if term in NOISE or term in kw:
        return
    if re.fullmatch(r'[\u4e00-\u9fff]{1,}', term):
        if len(term) < 2:
            return
        # 去掉以常见动词/助词结尾的碎片
        if re.search(r'[的了和与或把将给对在着过]', term[-1]) and len(term) > 3:
            term = term[:-1]
        if term in NOISE:
            return
    kw.append(term)


def auto_kw(desc, body=''):
    """从描述（+ 正文）里抽中文关键词。
    优先用『触发词：』『当用户…时使用』『用户要求「…」』，再兜底用正文里的 **加粗小标题**。"""
    kw = []
    d = desc

    # 1) 显式触发词
    for m in re.finditer(r'触发词[：:]\s*([^。\n]+)', d):
        for x in re.split(r'[、,，/／]', m.group(1)):
            x = x.strip(" 。.\"'")
            x = re.sub(r'^(只提供|提供|支持)\s*', '', x)
            _push(kw, x)

    # 2) 「当用户需要 A、B、C 时使用」
    for m in re.finditer(r'当用户[^。]{0,30}?时使用', d):
        seg = m.group(0)
        seg = re.sub(r'^当用户', '', seg)
        seg = re.sub(r'时使用$', '', seg)
        for x in re.split(r'[、,，/／]', seg):
            _push(kw, x)

    # 3) 「用户要求"A""B"」或「触发场景：A、B」
    for m in re.finditer(r'(?:触发场景|用户要求|适用于)[：:]?\s*([^。\n]{0,300})', d):
        seg = m.group(1)
        for x in re.split(r'[、,，/／]', seg):
            x = x.strip(" 。.\"'“”")
            x = re.sub(r'^问|^看', '', x)
            _push(kw, x)

    # 4) 「触发词」式列表段（顿号分隔的短句）
    if len(kw) < 5:
        for seg in re.split(r'[。；;\n]', d[:600]):
            if '、' not in seg:
                continue
            for x in re.split(r'[、]', seg):
                x = x.strip(" 。.\"'，")
                if 2 <= len(x) <= 8:
                    _push(kw, x)

    # 4b) 正文里的 **加粗小标题**（红狐系列的功能特性列表，路由信号很强）
    if len(kw) < 5 and body:
        for m in re.finditer(r'\*\*([^*\n]{2,16})\*\*', body[:2500]):
            _push(kw, m.group(1).strip())
            if len(kw) >= 8:
                break

    # 4c) 正文里的「触发词：」
    if len(kw) < 5 and body:
        for m in re.finditer(r'触发词[：:]\s*([^\n]{0,200})', body[:3000]):
            for x in re.split(r'[、,，/／]', m.group(1)):
                _push(kw, x.strip(" 。.\"'"))
            if len(kw) >= 8:
                break

    # 5) 英文描述 → 抽关键词
    if not kw:
        words = re.findall(r'[A-Za-z][A-Za-z0-9+-]{2,}', d[:300])
        seen = []
        for w in words:
            w = w.lower()
            if w in EN_STOP or w in seen:
                continue
            seen.append(w)
            kw.append(w)
            if len(kw) >= 8:
                break

    return kw[:9]


def auto_label(desc, name):
    d = desc.strip()
    # 去掉结尾的「当用户…时使用」补充句
    d = re.sub(r'当用户.*?时使用[。.]?', '', d).strip()
    seg = re.split(r'[。；;]', d)[0].strip()
    if len(seg) > 18:
        seg = re.split(r'[、，,：:]', seg)[0].strip()
    seg = re.sub(r'(工具|技能|skill)$', '', seg).strip()
    return (seg or name)[:20]


def clean(s):
    return s.replace('"', '').replace("'", '').replace('\\', '').strip()


def main():
    curated = dict(curated_zh.ZH)
    curated.update(curated_zh.ZH_NEW)

    skills = {}
    doms = os.path.join(ROOT, 'domains')
    for dom in sorted(os.listdir(doms)):
        dp = os.path.join(doms, dom)
        if not os.path.isdir(dp):
            continue
        for nm in sorted(os.listdir(dp)):
            p = os.path.join(dp, nm, 'SKILL.md')
            if os.path.isfile(p):
                skills[f'{dom}/{nm}'] = p

    out = {}
    auto_n = 0
    for key, p in skills.items():
        if key in curated:
            label, kws = curated[key]
            if isinstance(kws, str):
                kws = [k for k in kws.split(',') if k]
            out[key] = (clean(label), ','.join(clean(k) for k in kws))
            continue
        desc, body = get_desc(p)
        kws = auto_kw(desc, body)
        if kws:
            auto_n += 1
        out[key] = (clean(auto_label(desc, key.split('/')[1])),
                    ','.join(clean(k) for k in kws))

    missing = sorted(set(curated) - set(skills))
    print('技能总数 %d | 手工 %d | 自动 %d | curated 里多余的 %d'
          % (len(skills), len(skills) - auto_n, auto_n, len(missing)))
    if missing:
        print('  ⚠ curated 里没有对应技能的条目:', missing[:10])
    if A.check:
        return 0

    lines = ['# -*- coding: utf-8 -*-',
             '"""每个技能的中文标签 + 中文关键词 —— 由 gen_zh_keys.py 自动生成，请勿手工编辑。',
             '手工维护请改 curated_zh.py，然后重跑 python tools/gen_zh_keys.py',
             '"""',
             '',
             'ZH = {']
    cur = None
    for k in sorted(out):
        dom = k.split('/')[0]
        if dom != cur:
            cur = dom
            lines.append('\n# ---- %s ----' % dom)
        label, kws = out[k]
        lines.append('"%s": ("%s", "%s"),' % (k, label, kws))
    lines.append('}')
    with open(os.path.join(HERE, 'zh_keys.py'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    print('已写出 tools/zh_keys.py (%d 条)' % len(out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
