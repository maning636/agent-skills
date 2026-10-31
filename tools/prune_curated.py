#!/usr/bin/env python3
"""Prune curated_zh.py entries whose skill no longer exists, then regen zh_keys.py."""
import pathlib
import re
import subprocess
import sys
import json

ROOT = pathlib.Path(__file__).resolve().parent.parent
CURATED = ROOT / "tools" / "curated_zh.py"

live = set()
for p in (ROOT / "domains").rglob("SKILL.md"):
    rel = p.relative_to(ROOT / "domains").as_posix()
    dom, skill = rel.split("/")[0], rel.split("/")[-2]
    live.add(f"{dom}/{skill}")

text = CURATED.read_text(encoding="utf-8")
lines = text.split("\n")
out, dropped, retired = [], 0, {}
for line in lines:
    m = re.match(r'^\s*"([^"]+)"\s*:', line)
    if m and m.group(1) not in live:
        dropped += 1
        retired[m.group(1)] = line.strip()
        continue
    out.append(line)

CURATED.write_text("\n".join(out), encoding="utf-8")
print(f"curated_zh.py: dropped {dropped} stale entries, kept {len(out)} lines")

# 存档：被剔除的手工标签留底，将来复活技能可直接复用
RETIRED = ROOT / "tools" / "retired_zh.json"
if retired:
    old = {}
    if RETIRED.exists():
        old = json.loads(RETIRED.read_text(encoding="utf-8"))
    old.update(retired)
    RETIRED.write_text(
        json.dumps(old, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(f"retired_zh.json: 存档 {len(retired)} 条（累计 {len(old)} 条）")

r = subprocess.run([sys.executable, str(ROOT / "tools" / "gen_zh_keys.py")],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout.strip() or r.stderr.strip()[-2000:])
