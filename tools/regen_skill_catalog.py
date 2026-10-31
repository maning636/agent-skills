#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the machine-readable catalogs required by agent-workspace-spec 08 篇.

Outputs:
  <repo>/catalog.yaml                      library-level manifest (skills list)
  <repo>/domains/<domain>/catalog.yaml     per-domain manifest

Skill ids are `<domain>/<skill>` — the slash namespace keeps them unique across
libraries, while plugin skills use `plugin:<plugin>/<skill>` (colon namespace).

Fields beyond the 08 篇 baseline:
  authority      primary | fallback | superseded   (plugin coexistence)
  superseded_by  plugin skill that takes over
"""
import datetime
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
DOMAINS = os.path.join(ROOT, "domains")
TODAY = datetime.date.today().isoformat()

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def load_json(name):
    with open(os.path.join(TOOLS, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


def read_frontmatter(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read(6000)
    except Exception:
        return {}
    m = FM_RE.match(text)
    if not m:
        return {}
    data = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, _, v = line.partition(":")
        v = v.strip().strip('"').strip("'")
        data[k.strip()] = v
    return data


def zh_names():
    """<domain>/<skill> -> (中文名, 关键词) from tools/zh_keys.py"""
    out = {}
    path = os.path.join(TOOLS, "zh_keys.py")
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r'^\s*"([^"]+)"\s*:\s*\(\s*"(.*?)"\s*,\s*"(.*?)"\s*\)', line)
            if m:
                out[m.group(1)] = (m.group(2), m.group(3))
    return out


def collect():
    meta = load_json("domain_meta.json")
    overrides = load_json("skill_overrides.json")
    zh = zh_names()
    rows = []
    for dname in sorted(os.listdir(DOMAINS)):
        dpath = os.path.join(DOMAINS, dname)
        if not os.path.isdir(dpath):
            continue
        for name in sorted(os.listdir(dpath)):
            sk = os.path.join(dpath, name, "SKILL.md")
            if not os.path.isfile(sk):
                continue
            fm = read_frontmatter(sk)
            key = "%s/%s" % (dname, name)
            label, kws = zh.get(key, (name, ""))
            ov = overrides.get("skills", {}).get(key, {})
            row = {
                "id": key,
                "name": label,
                "path": "domains/%s/%s/SKILL.md" % (dname, name),
                "version": fm.get("version", "1.0.0"),
                "domain": dname,
                "description": fm.get("description", ""),
                "origin": fm.get("origin", "local"),
                "license": fm.get("license", ""),
                "tags": ov.get("tags", [dname]),
                "deprecated": False,
                "authority": ov.get("authority", "primary"),
            }
            if ov.get("superseded_by"):
                row["superseded_by"] = ov["superseded_by"]
            if kws:
                row["keywords"] = kws
            rows.append((dname, row))
    return meta, rows


def dump(path, data):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        yaml.safe_dump(data, fh, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=100)


def main():
    meta, rows = collect()
    by_domain = {}
    for dname, row in rows:
        by_domain.setdefault(dname, []).append(row)

    # 校验：skill_overrides.json / plugin_overlap.json 里的 key 必须指向真实存在的技能
    live_ids = {r["id"] for _d, r in rows}
    overrides = load_json("skill_overrides.json")
    for key in overrides.get("skills", {}):
        if key not in live_ids:
            print("!! skill_overrides.json 的 key 不存在: %s" % key)
    overlap = load_json("plugin_overlap.json")
    for row in overlap.get("overlap", []) + overlap.get("l0_rows", []):
        fb = row.get("fallback")
        if fb and fb not in live_ids:
            print("!! plugin_overlap.json 的 fallback 不存在: %s" % fb)

    # ---- library-level catalog.yaml -------------------------------------
    lib = {
        "version": 1,
        "kind": "skills",
        "library": "agent-skills",
        "updated": TODAY,
        "count": {"domains": len(by_domain), "skills": len(rows)},
        "domains": [],
        "skills": [],
    }
    for dname in sorted(by_domain):
        dm = meta["domains"].get(dname, {})
        entry = {
            "id": dname,
            "label": dm.get("label", dname),
            "path": "domains/%s" % dname,
            "catalog": "domains/%s/catalog.yaml" % dname,
            "index": "domains/%s/INDEX.md" % dname,
            "skills": len(by_domain[dname]),
            "authority": dm.get("authority", "domain"),
            "plugin_priority": bool(dm.get("plugin_priority")),
        }
        if dm.get("plugin_overlap"):
            entry["plugin_overlap"] = dm["plugin_overlap"]
        lib["domains"].append(entry)
    for _dname, row in rows:
        lib["skills"].append(dict(row))
    dump(os.path.join(ROOT, "catalog.yaml"), lib)

    # ---- per-domain catalogs -------------------------------------------
    for dname, drows in by_domain.items():
        dm = meta["domains"].get(dname, {})
        cat = {
            "version": 1,
            "kind": "skills",
            "library": "agent-skills",
            "domain": dname,
            "label": dm.get("label", dname),
            "updated": TODAY,
            "authority": dm.get("authority", "domain"),
            "plugin_priority": bool(dm.get("plugin_priority")),
            "count": {"skills": len(drows)},
            "skills": [dict(r) for r in drows],
        }
        if dm.get("plugin_overlap"):
            cat["plugin_overlap"] = dm["plugin_overlap"]
        dump(os.path.join(DOMAINS, dname, "catalog.yaml"), cat)

    print("catalog.yaml 已生成：%d 域 / %d 技能" % (len(by_domain), len(rows)))
    print("每域 catalog.yaml 已生成：%d 个" % len(by_domain))
    return 0


if __name__ == "__main__":
    sys.exit(main())
