# agent-skills

> **235 个岗位技能，按需远程加载，常驻上下文只有 ~1,290 tokens。**

一个给任意 Agent 用的技能库。设计上只让 Agent 常驻一张**领域路由表**，具体技能**用时再拉**——
不把 12.8 MB 技能正文整包塞进上下文。

```
常驻：   INDEX.md                    4.9 KB / ~1,290 tokens
按需：   domains/<域>/INDEX.md       0.6~9.6 KB（最多 ~2,600 tok）
按需：   domains/<域>/<技能>/SKILL.md 3~15 KB
────────────────────────────────────────────────────────────
整包读入（❌ 不要）： 12.8 MB / ~3,900,000 tokens
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
① 读 INDEX.md                        → 选领域（hr / product-management / sales / …）
② 读 domains/<领域>/INDEX.md         → 选技能（1~3 个）
③ 拉 domains/<领域>/<技能>/SKILL.md  → 执行
```

带缓存的取用脚本（`tools/fetch.py`，零依赖）：

```bash
python tools/fetch.py --index                           # L0 领域路由表
python tools/fetch.py --l1 human-resources              # L1 某领域技能清单
python tools/fetch.py --search "招聘 面试"               # 搜，返回候选 + 直链
python tools/fetch.py human-resources/interview-prep    # 取正文（命中缓存不发请求）
python tools/fetch.py --ls domains/legal/contract-review    # 看技能的附属文件
python tools/fetch.py --raw domains/legal/contract-review/references/x.md
python tools/fetch.py --cache-dir                       # 缓存位置
```

**完整协议见 [`FETCH.md`](FETCH.md)。**

---

## 库里有什么（22 个领域 / 235 个技能）

| 领域 | 技能数 | L1 大小 | 说明 |
|---|---:|---:|---|
| `small-business` | 44 | 9.6 KB | 经营快照、现金流、月结、报税、CRM、投标… |
| `sales` | 36 | 8.0 KB | 线索到赢单全流程、预测、CRM 卫生检查 |
| `agent-toolkit` | 15 | 3.7 KB | Office 文档、电脑操作、技能发现与调优、技能发布、PPT、多模态生成、联网抓取 |
| `opc` | 14 | 4.5 KB | **AI 一人公司**：赛道选择、价值主张、商业模式、MVP、转化闭环、获客、经营复盘、工具栈 |
| `growth-ops` | 13 | 3.7 KB | 目标拆解、假设验证、根因分析、同行顾问、决策评分、创意到回款 |
| `product-management` | 11 | 3.3 KB | PRD、路线图、竞品、指标；另含 HumanLayer `rpi` 全流程 |
| `data` | 10 | 2.4 KB | SQL、探查、统计、可视化、仪表盘 |
| `engineering` | 10 | 2.8 KB | 代码评审、调试、架构、故障应急、发版、测试策略、技术债 |
| `human-resources` | 9 | 2.5 KB | 招聘、面试、绩效、薪酬、组织 |
| `legal` | 9 | 2.3 KB | 合同、NDA、合规、法律风险、供应商审查 |
| `operations` | 9 | 2.3 KB | 流程文档、变更、风险、运行手册、容量规划 |
| `marketing` | 8 | 2.2 KB | 内容创作、邮件序列、SEO、品牌、竞品情报 |
| `finance` | 8 | 2.1 KB | 记账、对账、结账、报表、差异分析 |
| `understand` | 8 | 2.2 KB | 语义分析、差异理解、知识抽取、通俗解释、领域建模、上手引导 |
| `design` | 7 | 2.0 KB | 设计评审、无障碍、设计交付、设计系统、UX 文案 |
| `customer-support` | 5 | 1.5 KB | 工单分级、回复、升级、知识库 |
| `enterprise-search` | 5 | 1.4 KB | 跨源检索、知识综合、日报 |
| `hyperframes` | 5 | 1.8 KB | 网页动效引擎、转场、动效视频、网页转视频、动效注册表 |
| `productivity` | 4 | 1.2 KB | 任务管理、记忆管理、日常同步 |
| `cowork-plugin-management` | 2 | 0.9 KB | 插件创建与定制 |
| `local-tooling` | 2 | 1.1 KB | 离线 OCR 截图识文、Skill 调优评测 |
| `pdf-viewer` | 1 | 0.6 KB | PDF 批注、填表、签名 |

**共 235 个技能 / 1,661 个文件 / 12.81 MB**

| 来源批次 | 技能数 |
|---|---:|
| Anthropic `knowledge-work-plugins`（16 个插件，已排除 `bio-research`） | 184 |
| HumanLayer `skills`（rpi / show-me / visual-pr） | 3 |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | 5 |
| 本机自研（`agent-toolkit` / `growth-ops` / `understand` / `local-tooling` / OPC 体系） | 43 |
| **合计** | **235** |

---

## 为什么要这么设计

| | 传统 skill 机制 | 本库 |
|---|---|---|
| 常驻上下文 | 全部 skill 的 name+description ≈ **14,000 tok** | **~1,290 tok** |
| 取用方式 | 已经在 prompt 里，直接展开 | 按需拉取，单次 3~15 KB |
| 行为约束 | 强：进 prompt 就等于激活 | 弱：Agent 自己决定取不取 |
| 更新 | 要重新 import / 重启 | push 即生效，全员同步 |
| 可 review | 散在数据库里 | git PR，diff 清晰 |
| 跨 Agent | 绑定具体客户端 | 任何有网络+shell 的 Agent 都能用 |

---

## 内容来源与许可

| 来源 | 许可 | 收录内容 |
|---|---|---|
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Apache-2.0 | 除 `bio-research` 外全部 16 个插件（184 个技能） |
| [humanlayer/skills](https://github.com/humanlayer/skills) | MIT | `rpi` / `show-me` / `visual-pr`（3 个） |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | `hyperframes` 全套 + `website-to-hyperframes`（5 个） |
| 本机自研 | 见各技能 `license` 字段 | `agent-toolkit` `growth-ops` `understand` `local-tooling` `opc`（43 个） |

每个技能的 frontmatter 都带 `origin` 字段，标明精确来源路径与上游 commit。

本仓库聚合的是**上游已公开发布的第三方内容**，著作权归各自作者；
本仓库自身的脚本与索引以 MIT 发布（见 `LICENSE` / `NOTICE`）。

> **已剔除的非 MIT / 非商业内容**：飞书 `lark-suite`、企业微信 `wecom-suite`、宝玉 `baoyu-content`、
> 红狐 `redfox-*`（5 域）、`cad-3d`、`content-writing`、DBS `dbs-toolkit`（CC BY-NC 4.0）。
> 本仓库只保留 MIT / Apache-2.0 / 本机自研内容。

---

## 目录结构

```
agent-skills/
├── INDEX.md                 L0  领域路由表（唯一需要常驻的）
├── FETCH.md                 完整取用协议
├── CATALOG.md               全量技能目录（人读）
├── manifest.json            文件清单 + 大小（机器读）
├── LICENSE / NOTICE
├── domains/
│   └── <domain>/
│       ├── INDEX.md         L1  该领域的技能清单
│       └── <skill>/
│           ├── SKILL.md     L2  技能正文
│           └── references/  按需附属文件
└── tools/
    ├── fetch.py             带缓存的取用脚本（零依赖，--index/--l1/--search/--raw/--ls）
    ├── curated_zh.py        手工维护的中文标签/关键词表
    ├── gen_zh_keys.py       由 curated_zh + 技能描述生成 zh_keys.py
    ├── regen_manifest.py    重新生成 manifest.json
    └── regen_catalog.py     重新生成 CATALOG.md
```

---

## 扩充这个库

1. 把新技能放成 `domains/<domain>/<skill>/SKILL.md`，frontmatter 至少含 `name` / `description` / `origin`
2. 手工维护 `tools/curated_zh.py`，然后跑 `python tools/gen_zh_keys.py`
3. 跑 `python tools/regen_manifest.py` 与 `python tools/regen_catalog.py`
4. 更新根 `INDEX.md` 的领域路由表
5. push —— 所有 Agent 立刻可用，无需改任何客户端
