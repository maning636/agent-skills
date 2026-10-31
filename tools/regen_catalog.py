#!/usr/bin/env python3
"""Regenerate CATALOG.md from the surviving skills, preserving all curated labels.

- Reads the existing CATALOG.md to keep hand-written Chinese labels / keywords.
- Drops sections for removed domains and lines for removed skills.
- Rebuilds the top summary table with live counts.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "CATALOG.md"
META_FILE = ROOT / "tools" / "domain_meta.json"


def _load_domain_meta():
    """domain -> (中文名, 能做什么) from the single source of truth."""
    data = json.loads(META_FILE.read_text(encoding="utf-8"))
    return {
        d: (m.get("label", d), m.get("what", ""))
        for d, m in data["domains"].items()
    }


DOMAIN_META = _load_domain_meta()

SKILL_LINE = re.compile(r"^- \*\*(.+?)\*\* `([^`]+)` — ")


def live_skills():
    out = {}
    dom_root = ROOT / "domains"
    for d in sorted(dom_root.iterdir()):
        if not d.is_dir():
            continue
        out[d.name] = {p.parent.name for p in d.rglob("SKILL.md")}
    return out


def parse_catalog():
    """-> (dict domain -> list of lines, ordered domain list)"""
    text = CATALOG.read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.M)
    header = parts[0]
    sections = {}
    order = []
    for chunk in parts[1:]:
        first_line, _, body = chunk.partition("\n")
        m = re.match(r"(.+?) `([^`]+)`\s+—\s+(\d+) 个", first_line)
        if not m:
            continue
        domain = m.group(2)
        lines = [l for l in body.split("\n") if l.startswith("- **")]
        sections[domain] = lines
        order.append(domain)
    return header, sections, order


def build_opc_section(domain):
    """Build CATALOG lines for a domain from its INDEX.md table (label + keywords)."""
    idx = ROOT / "domains" / domain / "INDEX.md"
    lines = []
    for raw in idx.read_text(encoding="utf-8").split("\n"):
        if not raw.startswith("| `"):
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        name = cells[0].strip("`")
        label = cells[1]
        kw = cells[2]
        if " / " in kw:
            zh, en = kw.split(" / ", 1)
        else:
            zh, en = kw, ""
        desc = en.strip()
        lines.append(f"- **{label}** `{name}` — {zh.strip()}{(' / ' + desc) if desc else ''}")
    return sorted(lines)


def main():
    live = live_skills()
    header, sections, _ = parse_catalog()

    kept = {}
    for domain, lines in sections.items():
        if domain not in live:
            continue
        kept_lines = []
        for line in lines:
            m = SKILL_LINE.match(line)
            if not m:
                continue
            name = m.group(2)
            if name in live[domain]:
                kept_lines.append(line)
        if kept_lines:
            kept[domain] = kept_lines

    # domains that are live but had no section in CATALOG.md (e.g. opc)
    for domain in live:
        if domain not in kept and live[domain]:
            kept[domain] = build_opc_section(domain)

    ordered = sorted(
        kept,
        key=lambda d: (-len(kept[d]), DOMAIN_META.get(d, (d, ""))[0]),
    )

    out = ["# 技能总目录（%d 域 / %d 技能）\n" % (len(ordered), sum(len(v) for v in kept.values()))]
    out.append("| # | 域 | 能做什么 | 技能数 |")
    out.append("|---|---|---|---:|")
    for i, d in enumerate(ordered, 1):
        name, what = DOMAIN_META.get(d, (d, ""))
        out.append(f"| {i} | **{name}** `{d}` | {what} | {len(kept[d])} |")
    out.append("")

    for d in ordered:
        name, _ = DOMAIN_META.get(d, (d, ""))
        out.append(f"## {name} `{d}`  — {len(kept[d])} 个\n")
        out.extend(kept[d])
        out.append("")

    CATALOG.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"domains={len(ordered)} skills={sum(len(v) for v in kept.values())}")


if __name__ == "__main__":
    main()
