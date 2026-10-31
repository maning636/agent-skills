#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ground-truth audit of the repo: counts, origins, sizes.

Prints a JSON blob so doc numbers can be regenerated instead of hand-edited.
"""
import json
import os
import re
import sys
from collections import Counter, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAINS = os.path.join(ROOT, "domains")


def frontmatter(path):
    """Minimal YAML frontmatter reader (key: value, no nesting)."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            head = fh.read(4000)
    except Exception:
        return {}
    if not head.startswith("---"):
        return {}
    parts = head.split("---", 2)
    if len(parts) < 3:
        return {}
    out = OrderedDict()
    for line in parts[1].splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        v = v.strip().strip('"').strip("'")
        out[k.strip()] = v
    return out


def origin_bucket(origin):
    """Group an `origin:` frontmatter value into a source batch."""
    if not origin:
        return "unknown"
    o = origin.lower()
    if o.startswith("anthropics/"):
        return "anthropic"
    if o.startswith("humanlayer/"):
        return "humanlayer"
    if "hyperframes" in o:
        return "heygen"
    if o.startswith("local") or o.startswith("self"):
        return "local"
    return "other:" + origin.split("/")[0]


def main():
    domains = OrderedDict()
    origin_counts = Counter()
    skill_ids = []
    total_files = 0
    total_bytes = 0
    extra_files = Counter()

    for dname in sorted(os.listdir(DOMAINS)):
        dpath = os.path.join(DOMAINS, dname)
        if not os.path.isdir(dpath):
            continue
        skills = []
        l1 = os.path.join(dpath, "INDEX.md")
        l1_bytes = os.path.getsize(l1) if os.path.exists(l1) else 0
        dbytes = 0
        dfiles = 0
        for entry in sorted(os.listdir(dpath)):
            epath = os.path.join(dpath, entry)
            if not os.path.isdir(epath):
                continue
            skill_md = os.path.join(epath, "SKILL.md")
            if not os.path.exists(skill_md):
                extra_files["skill_without_md"] += 1
                continue
            fm = frontmatter(skill_md)
            bucket = origin_bucket(fm.get("origin", ""))
            origin_counts[bucket] += 1
            skills.append(entry)
            skill_ids.append("%s/%s" % (dname, entry))
            for root, _dirs, files in os.walk(epath):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        sz = os.path.getsize(fp)
                    except OSError:
                        continue
                    dbytes += sz
                    dfiles += 1
        # domain-level non-skill files (INDEX.md etc.)
        for root, _dirs, files in os.walk(dpath):
            for f in files:
                fp = os.path.join(root, f)
                rel = os.path.relpath(fp, dpath)
                if rel.count(os.sep) == 0:
                    dbytes += os.path.getsize(fp)
                    dfiles += 1
        domains[dname] = {
            "skills": len(skills),
            "skill_ids": skills,
            "l1_bytes": l1_bytes,
            "domain_bytes": dbytes,
            "domain_files": dfiles,
        }
        total_bytes += dbytes
        total_files += dfiles

    # repo-level files
    for f in sorted(os.listdir(ROOT)):
        fp = os.path.join(ROOT, f)
        if os.path.isfile(fp):
            total_bytes += os.path.getsize(fp)
            total_files += 1

    l0_path = os.path.join(ROOT, "INDEX.md")
    with open(l0_path, "rb") as fh:
        l0_raw = fh.read()
    l0_text = l0_raw.decode("utf-8")

    out = OrderedDict()
    out["domains"] = OrderedDict(
        (k, {kk: vv for kk, vv in v.items() if kk != "skill_ids"})
        for k, v in domains.items()
    )
    out["skill_total"] = sum(v["skills"] for v in domains.values())
    out["domain_total"] = len(domains)
    out["file_total"] = total_files
    out["bytes_total"] = total_bytes
    out["mb_total"] = round(total_bytes / 1048576, 2)
    out["l0_bytes"] = len(l0_raw)
    out["l0_lines"] = len(l0_text.splitlines())
    out["l0_tokens_est"] = round(len(l0_raw) / 3.85)
    out["origins"] = OrderedDict(sorted(origin_counts.items(), key=lambda kv: -kv[1]))
    out["origin_total"] = sum(origin_counts.values())
    out["skill_ids"] = skill_ids
    out["extra_files"] = dict(extra_files)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())
