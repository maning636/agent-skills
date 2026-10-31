#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hand the opc/* and growth-ops/* Chinese labels over to the new opc-playbook
library, then let prune_curated.py drop them from agent-skills.

Run BEFORE prune_curated.py, otherwise the labels are lost.
"""
import json
import os
import re
import sys

ROOT = r"D:\agent-skills"
CURATED = os.path.join(ROOT, "tools", "curated_zh.py")
OUT_DIR = r"D:\opc-playbook\tools"
OUT = os.path.join(OUT_DIR, "curated_zh.json")

PAT = re.compile(r'^\s*"([^"]+)"\s*:\s*\(\s*"(.*?)"\s*,\s*"(.*?)"\s*\)')

moved = {}
with open(CURATED, "r", encoding="utf-8") as fh:
    for line in fh:
        m = PAT.match(line)
        if not m:
            continue
        key, label, kws = m.groups()
        if key.startswith("opc/") or key.startswith("growth-ops/"):
            moved[key] = [label, kws]

if not moved:
    print("!! 没有找到 opc/ 或 growth-ops/ 的标签条目，检查 curated_zh.py")
    sys.exit(1)

os.makedirs(OUT_DIR, exist_ok=True)
payload = {
    "_comment": "opc-playbook 的中文标签表。键为 <组>/<技能名>，组为 opc 或 growth-ops。",
    "zh": {k: v for k, v in sorted(moved.items())},
}
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(payload, fh, ensure_ascii=False, indent=2)

print("已导出 %d 条中文标签 -> %s" % (len(moved), OUT))
for k, v in sorted(moved.items()):
    print("  %-34s %s" % (k, v[0]))
