#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Report the origin (provenance) distribution of every live skill.

Used to keep NOTICE / README numbers honest without hand-counting.
"""
import collections
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAINS = os.path.join(ROOT, "domains")
FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def fm_of(path):
    with open(path, "r", encoding="utf-8") as fh:
        t = fh.read(4000)
    m = FM.match(t)
    if not m:
        return {}
    d = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            d[k.strip()] = v.strip().strip('"')
    return d


def bucket(o):
    o = (o or "").lower()
    if o.startswith("anthropics/"):
        return "anthropic"
    if o.startswith("humanlayer/"):
        return "humanlayer"
    if "hyperframes" in o:
        return "heygen"
    return "self"


def main():
    by_bucket = collections.defaultdict(list)
    by_domain = collections.defaultdict(collections.Counter)
    for d in sorted(os.listdir(DOMAINS)):
        dp = os.path.join(DOMAINS, d)
        if not os.path.isdir(dp):
            continue
        for name in sorted(os.listdir(dp)):
            sk = os.path.join(dp, name, "SKILL.md")
            if not os.path.isfile(sk):
                continue
            o = fm_of(sk).get("origin", "")
            b = bucket(o)
            by_bucket[b].append((d + "/" + name, o))
            by_domain[d][b] += 1

    print("=== 来源批次 ===")
    for b, items in sorted(by_bucket.items(), key=lambda kv: -len(kv[1])):
        print("%-12s %d" % (b, len(items)))
        origins = collections.Counter(o for _, o in items)
        for o, n in origins.most_common():
            print("     %-70s %d" % (o, n))
    print()
    print("=== 按域 ===")
    for d in sorted(by_domain):
        print("%-26s %s" % (d, dict(by_domain[d])))
    print()
    print("总计: %d" % sum(len(v) for v in by_bucket.values()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
