#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild tools/retired_zh.json from git history.

Entries whose skill no longer exists are archived (label + keywords kept), so a
skill that comes back later can reuse its curated Chinese label instead of
falling back to auto-extraction.
"""
import json
import os
import re
import subprocess
import sys

ROOT = r"D:\agent-skills"
PAT = re.compile(r'^\s*"([^"]+)"\s*:\s*\(\s*"(.*?)"\s*,\s*"(.*?)"\s*\)')


def live_keys():
    out = set()
    doms = os.path.join(ROOT, "domains")
    for d in os.listdir(doms):
        dp = os.path.join(doms, d)
        if not os.path.isdir(dp):
            continue
        for name in os.listdir(dp):
            if os.path.isfile(os.path.join(dp, name, "SKILL.md")):
                out.add("%s/%s" % (d, name))
    return out


def main():
    live = live_keys()
    raw = subprocess.run(
        ["git", "-C", ROOT, "show", "HEAD:tools/curated_zh.py"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if raw.returncode != 0:
        print("读取 git 历史失败：", raw.stderr[-500:])
        return 2

    retired = {}
    for line in raw.stdout.splitlines():
        m = PAT.match(line)
        if not m:
            continue
        key, label, kws = m.groups()
        if key not in live:
            retired[key] = [label, kws]

    out_path = os.path.join(ROOT, "tools", "retired_zh.json")
    payload = {
        "_comment": "已剔除技能的中文标签存档。复活技能时从这里取回，避免标签质量退化。",
        "zh": retired,
    }
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    print("retired_zh.json: 存档 %d 条" % len(retired))
    for k in sorted(retired):
        print("  %-42s %s" % (k, retired[k][0]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
