#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract domains/opc + domains/growth-ops from agent-skills into a standalone
`opc-playbook` library (layout follows agent-workspace-spec 08 篇:
`skills/<name>/SKILL.md` + root `catalog.yaml`).

- copies each skill dir verbatim (assets/scripts included)
- rewrites frontmatter `id:` to the globally-unique `opc-playbook/<name>`
- keeps `domain:` so the two internal groups (opc / growth-ops) survive
"""
import os
import re
import shutil
import sys

SRC_ROOT = r"D:\agent-skills"
DST_ROOT = r"D:\opc-playbook"
GROUPS = ["opc", "growth-ops"]
LIB = "opc-playbook"


def rewrite_frontmatter(skill_md):
    with open(skill_md, "r", encoding="utf-8", newline="") as fh:
        text = fh.read()
    if not text.startswith("---"):
        return False
    parts = text.split("---", 2)
    if len(parts) < 3:
        return False
    fm = parts[1]
    new_fm, n = re.subn(
        r"^id:\s*(opc|growth-ops)/(.+?)\s*$",
        r"id: %s/\2" % LIB,
        fm,
        flags=re.M,
    )
    if n == 0:
        return False
    with open(skill_md, "w", encoding="utf-8", newline="") as fh:
        fh.write("---" + new_fm + "---" + parts[2])
    return True


def main():
    moved = []
    for group in GROUPS:
        src_dir = os.path.join(SRC_ROOT, "domains", group)
        if not os.path.isdir(src_dir):
            print("skip missing group:", group)
            continue
        for name in sorted(os.listdir(src_dir)):
            src = os.path.join(src_dir, name)
            if not os.path.isdir(src):
                continue
            dst = os.path.join(DST_ROOT, "skills", name)
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            skill_md = os.path.join(dst, "SKILL.md")
            ok = rewrite_frontmatter(skill_md) if os.path.exists(skill_md) else False
            moved.append((group, name, ok))
            print("%-10s %-28s id-rewrite=%s" % (group, name, ok))
    print("\n共迁移 %d 个技能 -> %s" % (len(moved), DST_ROOT))


if __name__ == "__main__":
    sys.exit(main())
