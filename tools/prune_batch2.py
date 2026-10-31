#!/usr/bin/env python3
"""Batch-2 prune: drop skills that have a substitute in engineering-standard /
design-skills-playbook / agent-workspace-spec, and strip their rows from the L1 index."""
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(r"D:\agent-skills")

# domain -> skills to delete (each has a documented substitute)
DROP = {
    "engineering": [
        "architecture",        # engineering-standard ARCH-PATTERNS.md + PLAYBOOK §7.1
        "code-review",         # engineering-standard PROJECT-RUN/CRAFTS/REVIEW.md
        "deploy-checklist",    # engineering-standard PROJECT-RUN/RELEASE.md §1/§3 + P4/P5
        "documentation",       # engineering-standard PLAYBOOK §4 文档分层
        "incident-response",   # engineering-standard AGENT-PROTOCOL P6 + PLAYBOOK §3.5
        "system-design",       # engineering-standard ARCH-PATTERNS.md
        "tech-debt",           # engineering-standard PLAYBOOK §4.4 防漂移 + §9 检查单
        "testing-strategy",    # engineering-standard CRAFTS/TDD.md + CRAFTS/VERIFY.md + §5 质量门禁
    ],
    "understand": [
        "understand-onboard",  # engineering-standard §4 文档分层 / AGENTS.md 新人上手
    ],
    "marketing": [
        "content-creation",    # 自媒体内容创作（本库已删 content-writing 域）
        "draft-content",       # 自媒体内容创作
        "mkt-competitive-brief",  # sales/competitive-intelligence + product-management/pm-competitive-brief
        "performance-report",  # small-business/report-builder + report-pack
        "seo-audit",           # small-business/seo-ai-visibility + content-strategy
    ],
    "product-management": [
        "pm-competitive-brief",   # sales/competitive-intelligence
        "product-brainstorming",  # opc-orchestrator + growth-ops 六顶帽/第一性原理
        "rpi",                   # PRD 味（用户明确不要 PRD）；与 write-spec 同族
        "show-me",               # design-skills-playbook/scene-1-show-me 完全重复
        "sprint-planning",       # engineering-standard P3 开发循环 + 拆入任务栈
        "synthesize-research",   # design/research-synthesis
        "visual-pr",             # engineering-standard CRAFTS/REVIEW.md
        "write-spec",            # PRD 味（用户明确不要 PRD）
    ],
}

ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|")


def main():
    removed = 0
    for domain, skills in DROP.items():
        for skill in skills:
            d = ROOT / "domains" / domain / skill
            if not d.exists():
                print(f"  skip (absent): {domain}/{skill}")
                continue
            r = subprocess.run(["git", "rm", "-r", "-q", f"domains/{domain}/{skill}"],
                               cwd=ROOT, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"  git rm failed: {domain}/{skill}: {r.stderr.strip()[:120]}")
                continue
            if d.exists():  # leftover untracked junk (.DS_Store etc.)
                shutil.rmtree(d, ignore_errors=True)
            removed += 1

        # strip rows from the L1 index
        idx = ROOT / "domains" / domain / "INDEX.md"
        if idx.exists():
            lines = idx.read_text(encoding="utf-8").split("\n")
            out = []
            for line in lines:
                m = ROW.match(line)
                if m and m.group(1) in skills:
                    continue
                out.append(line)
            text = "\n".join(out)
            n = len([l for l in out if ROW.match(l)])
            text = re.sub(r"\*\*技能数\*\*：\d+", f"**技能数**：{n}", text)
            text = re.sub(r"\*\*技能数\*\*:\s*\d+", f"**技能数**：{n}", text)
            idx.write_text(text, encoding="utf-8")
            print(f"  {domain}/INDEX.md -> {n} skills")

    print(f"removed {removed} skills")


if __name__ == "__main__":
    main()
