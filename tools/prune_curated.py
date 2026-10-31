#!/usr/bin/env python3
"""Prune curated_zh.py entries whose skill no longer exists, then regen zh_keys.py."""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CURATED = ROOT / "tools" / "curated_zh.py"

live = set()
for p in (ROOT / "domains").rglob("SKILL.md"):
    rel = p.relative_to(ROOT / "domains").as_posix()
    dom, skill = rel.split("/")[0], rel.split("/")[-2]
    live.add(f"{dom}/{skill}")

text = CURATED.read_text(encoding="utf-8")
lines = text.split("\n")
out, dropped = [], 0
for line in lines:
    m = re.match(r'^\s*"([^"]+)"\s*:', line)
    if m and m.group(1) not in live:
        dropped += 1
        continue
    out.append(line)

CURATED.write_text("\n".join(out), encoding="utf-8")
print(f"curated_zh.py: dropped {dropped} stale entries, kept {len(out)} lines")

r = subprocess.run([sys.executable, str(ROOT / "tools" / "gen_zh_keys.py")],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout.strip() or r.stderr.strip()[-2000:])
