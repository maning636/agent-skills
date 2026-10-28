# agent-skills

> **178 个岗位技能，按需远程加载，常驻上下文只有 ~1,000 tokens。**

一个给任意 Agent 用的技能库。设计上只让 Agent 常驻一张**领域路由表**，具体技能**用时再拉**——
不把 2.7 MB 技能正文整包塞进上下文。

```
常驻：   INDEX.md            44 行 / 3.5 KB / ~990 tokens
按需：   domains/<域>/INDEX.md        0.3~4.8 KB（最多 ~1,600 tok）
按需：   domains/<域>/<技能>/SKILL.md  3~15 KB
────────────────────────────────────────────────
整包读入（❌ 不要）： 2.7 MB / ~700,000 tokens
```

---

## 给 Agent 的用法（核心）

**第一步，把下面这一行放进你的常驻上下文**（CLAUDE.md / AGENTS.md / 系统提示）：

```
技能库：https://raw.githubusercontent.com/maning636/agent-skills/main/INDEX.md
取用协议：https://raw.githubusercontent.com/maning636/agent-skills/main/FETCH.md
```

或者直接给 Agent 这一段**更省事的指令**（推荐，效果等同）：

```
你有一个远程岗位技能库，入口 https://raw.githubusercontent.com/maning636/agent-skills/main/INDEX.md
（先读它，再按其中的「取用三步」按需拉取 domains/<领域>/INDEX.md 与 domains/<领域>/<技能>/SKILL.md）。
硬规则：一次只取 1~3 个技能；禁止整包下载整个仓库；技能正文必须来自上面的 URL，不得凭记忆编造流程。
需要中文检索时用 python tools/fetch.py --search "<关键词>"（克隆后可用）或直接读 L1 的「关键词」列比对。
```

**第二步，Agent 自己去取：**

```
① 读 INDEX.md                        → 选领域（hr / product-management / engineering / …）
② 读 domains/<领域>/INDEX.md         → 选技能（1~3 个）
③ 拉 domains/<领域>/<技能>/SKILL.md  → 执行
```

带缓存的取用脚本（`tools/fetch.py`，零依赖）：

```bash
python tools/fetch.py --search "招聘 面试"          # 搜，返回候选 + 直链
python tools/fetch.py human-resources/interview-prep # 取正文（命中缓存不发请求）
python tools/fetch.py --cache-dir                    # 缓存位置
```

**完整协议见 [`FETCH.md`](FETCH.md)。**

---

## 库里有什么

| 领域 | 技能数 | 说明 |
|---|---:|---|
| `human-resources` | 9 | 招聘、面试、绩效、薪酬、组织 |
| `product-management` | 11 | PRD、路线图、竞品、指标；另含 HumanLayer `rpi` 全流程 |
| `engineering` | 10 | 代码评审、调试、架构、故障应急、发版 |
| `design` | 7 | 设计评审、无障碍、设计交付、设计系统、UX 文案 |
| `marketing` | 8 | 内容创作、邮件序列、SEO、品牌 |
| `sales` | 36 | 线索到赢单全流程、预测、CRM |
| `legal` | 9 | 合同、NDA、合规、法律风险 |
| `finance` | 8 | 记账、对账、结账、报表、差异分析 |
| `operations` | 9 | 流程文档、变更、风险、运行手册 |
| `customer-support` | 5 | 工单分级、回复、升级、知识库 |
| `data` | 10 | SQL、探查、统计、可视化、仪表盘 |
| `enterprise-search` | 5 | 跨源检索、知识综合、日报 |
| `productivity` | 4 | 任务管理、记忆管理、日常同步 |
| `small-business` | 44 | 经营快照、现金流、月结、报税、CRM、投标… |
| `cowork-plugin-management` | 2 | 插件创建与定制 |
| `pdf-viewer` | 1 | PDF 批注、填表、签名 |

**共 178 个技能 / 444 个文件 / 2.7 MB。**

---

## 为什么要这么设计

| | 传统 skill 机制 | 本库 |
|---|---|---|
| 常驻上下文 | 全部 skill 的 name+description ≈ **10,524 tok** | **~990 tok** |
| 取用方式 | 已经在 prompt 里，直接展开 | 按需拉取，单次 3~15 KB |
| 行为约束 | 强：进 prompt 就等于激活 | 弱：Agent 自己决定取不取 |
| 更新 | 要重新 import / 重启 | push 即生效，全员同步 |
| 可 review | 散在数据库里 | git PR，diff 清晰 |
| 跨 Agent | 绑定具体客户端 | 任何有网络+shell 的 Agent 都能用 |

---

## 内容来源与许可

| 来源 | 许可 | 收录内容 |
|---|---|---|
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Apache-2.0 | 除 `bio-research` 外全部 16 个插件 |
| [humanlayer/skills](https://github.com/humanlayer/skills) | MIT | `rpi` / `show-me` / `visual-pr` |

每个技能的 frontmatter 都带 `origin` 字段，标明精确来源路径与上游 commit。

本仓库聚合的是**上游已公开发布的第三方内容**，著作权归各自作者；
本仓库自身的脚本与索引以 MIT 发布（见 `LICENSE` / `NOTICE`）。

---

## 目录结构

```
agent-skills/
├── INDEX.md                 L0  领域路由表（唯一需要常驻的）
├── FETCH.md                 完整取用协议
├── manifest.json            文件清单 + 大小（机器读）
├── LICENSE / NOTICE
├── domains/
│   └── <domain>/
│       ├── INDEX.md         L1  该领域的技能清单
│       └── <skill>/
│           ├── SKILL.md     L2  技能正文
│           └── references/  按需附属文件
└── tools/
    └── fetch.py             带缓存的取用脚本（零依赖）
```

---

## 扩充这个库

1. 把新技能放成 `domains/<domain>/<skill>/SKILL.md`，frontmatter 至少含 `name` / `description`
2. 重新生成 L1 索引和 `manifest.json`
3. push —— 所有 Agent 立刻可用，无需改任何客户端
