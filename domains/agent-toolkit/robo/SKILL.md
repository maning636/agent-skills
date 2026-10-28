---
id: agent-toolkit/robo
domain: agent-toolkit
name: robo
description: "ROBONUGGETS Skills Bundle — 整合 plan-for-goal, calibrate, personalise, tweak, html-it 五个技能。输入 /robo 或 'robo技能' 时调用。"
author: "@robonuggets"
origin: 本机自研
license: 见来源
---


# ROBONUGGETS Skills Bundle

整合以下五个技能，统一入口。

## 包含技能（位于 `~/.kimi/skills/robo/`）

| 技能 | 触发词 | 说明 |
|------|--------|------|
| `plan-for-goal` | /plan-for-goal, "plan for goal" | 将需求转化为结构化计划 |
| `calibrate` | "校准", calibrate | 会话内自我改进 |
| `personalise` | "个性化", personalise | 将外部内容适配到你的环境 |
| `tweak` | "微调", tweak | 交互式 CSS 参数调整面板 |
| `html-it` | /html-it, "html this" | HTML 输出替代 Markdown |

## 调用方式

根据用户需求，选择最合适的子技能调用：

- 需要做计划 → 加载 `plan-for-goal`
- 需要校准自身表现 → 加载 `calibrate`
- 需要适配外部内容 → 加载 `personalise`
- 需要调整 CSS 参数 → 加载 `tweak`
- 需要 HTML 输出 → 加载 `html-it`

## 来源

- robonuggets/plan-for-goal
- robonuggets/skills (calibrate, personalise, tweak)
- robonuggets/html-it