#!/usr/bin/env python3
"""Regenerate manifest.json for the agent-skills repo (three-tier progressive disclosure).

- total_skills : number of SKILL.md files under domains/
- domains      : per-domain { index, skills }
- files        : every tracked file under domains/ and tools/ with its byte size
"""
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "manifest.json"

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}


def collect_files():
    files = []
    # repo root documents (README / INDEX / FETCH / CATALOG / catalog.yaml / NOTICE / AGENT ...)
    for p in sorted(ROOT.iterdir()):
        if p.is_file() and p.name not in {".DS_Store"}:
            files.append({"path": p.name, "bytes": p.stat().st_size})
    for sub in ("domains", "tools"):
        base = ROOT / sub
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            files.append({"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size})
    return files


def main():
    domains = {}
    total_skills = 0
    dom_root = ROOT / "domains"
    for d in sorted(dom_root.iterdir()):
        if not d.is_dir():
            continue
        n = sum(1 for _ in d.rglob("SKILL.md"))
        domains[d.name] = {
            "index": f"domains/{d.name}/INDEX.md",
            "skills": n,
        }
        total_skills += n

    files = collect_files()
    l0 = ROOT / "INDEX.md"
    l0_bytes = l0.stat().st_size
    manifest = {
        "name": "agent-skills",
        "version": "1.0.0",
        "layout": "three-tier-progressive-disclosure",
        "l0": "INDEX.md",
        "l0_bytes": l0_bytes,
        "l0_tokens_est": round(l0_bytes / 3.85),
        "domains": domains,
        "files": files,
        "total_skills": total_skills,
        "total_files": len(files),
        "total_bytes": sum(f["bytes"] for f in files),
        "raw_base": "https://raw.githubusercontent.com/maning636/agent-skills/main/",
    }
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"domains={len(domains)} skills={total_skills} files={len(files)} "
          f"bytes={manifest['total_bytes']} l0_bytes={manifest['l0_bytes']}")


if __name__ == "__main__":
    main()
