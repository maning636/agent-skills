#!/usr/bin/env python3
"""Regenerate CATALOG.md from the surviving skills, preserving all curated labels.

- Reads the existing CATALOG.md to keep hand-written Chinese labels / keywords.
- Drops sections for removed domains and lines for removed skills.
- Rebuilds the top summary table with live counts.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "CATALOG.md"

# domain -> (中文名, 能做什么)
DOMAIN_META = {
    "small-business": ("小企业 / 团队经营", "经营快照,现金流,月结,报税,CRM"),
    "sales": ("销售", "线索,商机,报价,赢单,预测"),
    "opc": ("AI 一人公司", "赛道选择,价值主张,商业模式,MVP,转化闭环,获客,经营复盘"),
    "product-management": ("产品管理", "PRD,需求,路线图,竞品,指标"),
    "engineering": ("研发 / 工程", "代码评审,调试,架构,故障,发版"),
    "data": ("数据 / 数据科学", "SQL,数据探查,统计,可视化,仪表盘"),
    "human-resources": ("人力资源 / HR", "招聘,面试,绩效,薪酬,入职"),
    "legal": ("法务 / 合规", "合同,NDA,合规,法律风险"),
    "operations": ("运营", "流程文档,变更,风险,运行手册"),
    "marketing": ("市场 / 营销", "内容创作,邮件序列,SEO,品牌"),
    "finance": ("财务", "记账,对账,结账,报表,差异分析"),
    "understand": ("语义理解", "语义分析,差异理解,知识抽取,通俗解释"),
    "design": ("设计", "设计评审,无障碍,设计交付,设计系统"),
    "customer-support": ("客户支持", "工单,回复,升级,知识库"),
    "enterprise-search": ("企业搜索", "跨源检索,知识综合,日报"),
    "hyperframes": ("HyperFrames 动效", "网页动效,动效引擎,转场,网页转视频"),
    "agent-toolkit": ("Agent 工具箱", "Office文档,电脑操作,技能发现与调优,PPT,多模态生成,联网抓取"),
    "productivity": ("个人生产力", "任务管理,记忆管理,日常同步"),
    "growth-ops": ("商业与增长", "目标拆解,假设验证,根因分析,同行顾问,决策评分,创意到回款"),
    "local-tooling": ("本机工具", "离线OCR,截图识文,Skill调优"),
    "cowork-plugin-management": ("插件 / 技能工程", "创建插件,定制插件"),
    "pdf-viewer": ("PDF 处理", "PDF,批注,填表,签名"),
}

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
