# agent-skills

> **453 个岗位技能，按需远程加载，常驻上下文只有 ~1,670 tokens。**

一个给任意 Agent 用的技能库。设计上只让 Agent 常驻一张**领域路由表**，具体技能**用时再拉**——
不把 58 MB 技能正文整包塞进上下文。

```
常驻：   INDEX.md                    60 行 / 6.4 KB / ~1,670 tokens
按需：   domains/<域>/INDEX.md       0.6~9.7 KB（最多 ~2,700 tok）
按需：   domains/<域>/<技能>/SKILL.md 3~15 KB
────────────────────────────────────────────────────────────
整包读入（❌ 不要）： 58 MB / ~14,000,000 tokens
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
① 读 INDEX.md                        → 选领域（hr / product-management / lark-suite / …）
② 读 domains/<领域>/INDEX.md         → 选技能（1~3 个）
③ 拉 domains/<领域>/<技能>/SKILL.md  → 执行
```

带缓存的取用脚本（`tools/fetch.py`，零依赖）：

```bash
python tools/fetch.py --search "招聘 面试"           # 搜，返回候选 + 直链
python tools/fetch.py human-resources/interview-prep # 取正文（命中缓存不发请求）
python tools/fetch.py --cache-dir                    # 缓存位置
```

**完整协议见 [`FETCH.md`](FETCH.md)。**

---

## 库里有什么（32 个领域 / 453 个技能）

| 领域 | 技能数 | L1 大小 | 说明 |
|---|---:|---:|---|
| `small-business` | 44 | 9.7 KB | 经营快照、现金流、月结、报税、CRM、投标… |
| `growth-ops` | 38 | 9.4 KB | 竞品分析、客户情报、KPI 看板、销售漏斗、市场情报、决策系统、OPC 商业设计 |
| `sales` | 36 | 8.1 KB | 线索到赢单全流程、预测、CRM |
| `agent-toolkit` | 30 | 7.9 KB | 网页动画、HTML 生成、前端设计、Office 文档、电脑操作、技能发现、CLI 工具 |
| `lark-suite` | 28 | 7.1 KB | **飞书全套**：消息、日历、文档、多维表格、电子表格、任务、知识库、审批、妙记、OKR |
| `redfox-multi` | 25 | 8.3 KB | 红狐通用能力：多平台聚合、AI 搜索、热点榜、股票研报、视频下载、生图生视频 |
| `dbs-toolkit` | 21 | 4.2 KB | 商业模式、执行力、拖延、AI 味检测、对标、目标澄清、概念拆解、决策系统、交互式学习 |
| `baoyu-content` | 21 | 5.5 KB | **宝玉内容全家桶**：文章配图、封面、信息图、漫画、演示稿、翻译、发布到公众号/微博/X |
| `redfox-wechat` | 21 | 7.5 KB | 红狐·公众号：搜索、10w 热文、涨粉最快、原创榜、标题、封面、排版、违禁词 |
| `redfox-xiaohongshu` | 19 | 7.1 KB | 红狐·小红书：搜笔记、笔记分析、账号诊断、选题、标题、封面、违禁词、榜单 |
| `redfox-douyin` | 15 | 6.2 KB | 红狐·抖音：搜索、热榜、涨粉榜、账号诊断、订阅、违禁词、作品抓取 |
| `cad-3d` | 14 | 3.5 KB | CAD 建模、DXF、工程图、STEP、URDF、G-code、DFM、3D 打印、3D 产品图 |
| `wecom-suite` | 14 | 4.6 KB | **企业微信全套**：消息、日程、邮件、文档、表格、待办、通讯录、微盘、在线会议 |
| `product-management` | 11 | 3.3 KB | PRD、路线图、竞品、指标；另含 HumanLayer `rpi` 全流程 |
| `engineering` | 10 | 2.8 KB | 代码评审、调试、架构、故障应急、发版 |
| `data` | 10 | 2.5 KB | SQL、探查、统计、可视化、仪表盘 |
| `human-resources` | 9 | 2.5 KB | 招聘、面试、绩效、薪酬、组织 |
| `legal` | 9 | 2.3 KB | 合同、NDA、合规、法律风险 |
| `operations` | 9 | 2.3 KB | 流程文档、变更、风险、运行手册 |
| `marketing` | 8 | 2.3 KB | 内容创作、邮件序列、SEO、品牌 |
| `finance` | 8 | 2.1 KB | 记账、对账、结账、报表、差异分析 |
| `understand` | 8 | 2.2 KB | 语义分析、差异理解、知识抽取、通俗解释、领域建模、上手引导 |
| `design` | 7 | 2.1 KB | 设计评审、无障碍、设计交付、设计系统、UX 文案 |
| `content-writing` | 7 | 2.9 KB | 人味写作、去 AI 味、大字海报、内容图谱、知识星球、Prism 内容、创作工具 |
| `redfox-bilibili` | 7 | 3.4 KB | 红狐·B站：搜索、UP主作品、评论、关键词账号 |
| `customer-support` | 5 | 1.5 KB | 工单分级、回复、升级、知识库 |
| `enterprise-search` | 5 | 1.4 KB | 跨源检索、知识综合、日报 |
| `hyperframes` | 5 | 1.8 KB | 网页动效引擎、转场、动效视频、网页转视频、动效注册表 |
| `productivity` | 4 | 1.2 KB | 任务管理、记忆管理、日常同步 |
| `cowork-plugin-management` | 2 | 0.9 KB | 插件创建与定制 |
| `local-tooling` | 2 | 1.1 KB | 离线 OCR 截图识文、Skill 调优评测 |
| `pdf-viewer` | 1 | 0.6 KB | PDF 批注、填表、签名 |

**共 453 个技能 / 4,636 个文件 / 57.90 MB**

| 来源批次 | 技能数 |
|---|---:|
| Anthropic `knowledge-work-plugins`（已排除 `bio-research`） | 175 |
| HumanLayer `skills`（rpi / show-me / visual-pr） | 3 |
| 本机 `.agents/skills` 活跃目录 | 57 |
| 本机 `.agents/skills` 4 个历史备份目录 | 218 |
| **合计** | **453** |

---

## 为什么要这么设计

| | 传统 skill 机制 | 本库 |
|---|---|---|
| 常驻上下文 | 全部 skill 的 name+description ≈ **27,000 tok** | **~1,670 tok** |
| 取用方式 | 已经在 prompt 里，直接展开 | 按需拉取，单次 3~15 KB |
| 行为约束 | 强：进 prompt 就等于激活 | 弱：Agent 自己决定取不取 |
| 更新 | 要重新 import / 重启 | push 即生效，全员同步 |
| 可 review | 散在数据库里 | git PR，diff 清晰 |
| 跨 Agent | 绑定具体客户端 | 任何有网络+shell 的 Agent 都能用 |

---

## 内容来源与许可

| 来源 | 许可 | 收录内容 |
|---|---|---|
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Apache-2.0 | 除 `bio-research` 外全部 16 个插件（175 个技能） |
| [humanlayer/skills](https://github.com/humanlayer/skills) | MIT | `rpi` / `show-me` / `visual-pr`（3 个） |
| [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad) | MIT | `cad` `dxf` `sdf` `srdf` `urdf` `gcode` `step-parts` `sendcutsend` `engineering-drawing` `dfm` `dfam-check`（11 个） |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | `hyperframes` 全套 + `website-to-hyperframes`（5 个） |
| [unnoo/zsxq-skill](https://github.com/unnoo/zsxq-skill) | MIT | `zsxq`（1 个） |
| 飞书官方 `open.feishu.cn` | MIT | `lark-suite`（28 个） |
| [WeComTeam/wecom-cli](https://github.com/WeComTeam/wecom-cli) | MIT | `wecom-suite`（14 个） |
| [baoyu-skills](https://github.com/baoyu-skills)（宝玉） | MIT | `baoyu-content`（21 个） |
| [redfox-data/redfox-community](https://github.com/redfox-data/redfox-community) | 见各技能 | `redfox-*` 五个域（87 个） |
| 本机自研 | 见各技能 `license` 字段 | `dbs-toolkit` `understand` `content-writing` `growth-ops` `agent-toolkit` `cad-3d` 等 |

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
    ├── fetch.py             带缓存的取用脚本（零依赖）
    ├── curated_zh.py        手工维护的中文标签/关键词表
    └── gen_zh_keys.py       由 curated_zh + 技能描述生成 zh_keys.py
```

---

## 扩充这个库

1. 把新技能放成 `domains/<domain>/<skill>/SKILL.md`，frontmatter 至少含 `name` / `description`
2. 手工维护 `tools/curated_zh.py`，然后跑 `python tools/gen_zh_keys.py`
3. 重新生成 L1 索引和 `manifest.json`
4. push —— 所有 Agent 立刻可用，无需改任何客户端
