# agent-skills

> **企业职能技能库** —— 186 个技能 / 20 个领域 / 三层渐进披露。
> **唯一常驻进上下文的是 `INDEX.md`（约 1.9k tokens）；其余 186 个技能正文全部按需拉取。**

---

## 这是什么

一套**给 Agent 按需查**的企业职能技能库。覆盖财务、销售、法务、HR、运营、客服、数据、
企业搜索、设计、代码理解、动效视频等日常事务。

| 指标 | 值 |
|---|---|
| 技能数 | **186** |
| 领域数 | **20** |
| 文件数 | 1,475 |
| 库大小 | 11.8 MB |
| **L0 常驻开销** | **7,407 B ≈ 1,924 tokens** |
| 整包读入的开销 | 11.8 MB ≈ **3.22M tokens**（约 3.5 万倍） |

**这就是为什么不能整包装载。** L0 只占整包的 0.06%。

---

## 取用三步

1. 读 `INDEX.md` → 按任务选出 1~2 个候选领域
2. 读 `domains/<领域>/INDEX.md` → 选出 1~3 个具体技能
3. **只拉取那几个 `SKILL.md`**，其余一律不取

```bash
python tools/fetch.py --index                    # 取 L0
python tools/fetch.py --l1 engineering            # 取某域 L1
python tools/fetch.py --search 现金流             # 定位技能
python tools/fetch.py --raw domains/finance/cash-flow-snapshot/SKILL.md
python tools/fetch.py --cache-clear               # 一键清缓存
```

零依赖，只用 Python 标准库。首次取用后缓存在 `~/.cache/agent-skills/`，网络失败自动降级到缓存。

---

## 目录结构

```
agent-skills/
├─ INDEX.md                 L0 路由表（唯一常驻，7.4 KB）
├─ catalog.yaml             机器可读清单（库级，含 authority / superseded_by）
├─ AGENT.md                 给 Agent 读的使用契约
├─ FETCH.md                 取用协议 + 命令
├─ CATALOG.md               人类可读总目录（中文名 + 触发词）
├─ manifest.json            文件级清单
├─ NOTICE                   出处与许可
├─ LICENSE                  MIT（本库原创部分）
├─ domains/<域>/INDEX.md          L1
├─ domains/<域>/catalog.yaml      该域机器可读清单
├─ domains/<域>/<技能>/SKILL.md   L2
└─ tools/
   ├─ fetch.py                    取用脚本（零依赖）
   ├─ domain_meta.json            领域元信息（唯一真相源）
   ├─ plugin_overlap.json         插件覆盖对照
   ├─ curated_zh.py / zh_keys.py  中文名与触发词
   ├─ retired_zh.json             已剔除技能的中文标签存档
   ├─ regen_index.py              重生成 INDEX.md
   ├─ regen_skill_catalog.py      重生成 catalog.yaml（顶层 + 每域）
   ├─ regen_catalog.py            重生成 CATALOG.md
   ├─ regen_manifest.py           重生成 manifest.json
   ├─ prune_curated.py            清理失效标签
   ├─ origin_report.py            出处分布报告
   ├─ audit_truth.py              数量真值审计
   ├─ handoff_zh_labels.py        迁出标签交接
   └─ extract_opc_playbook.py     迁出 OPC 域
```

---

## 内容来源与许可

| 来源 | 技能数 | 许可 |
|---|---:|---|
| Anthropic `knowledge-work-plugins` | 157 | Apache-2.0 |
| 本机自研（agent-toolkit 15 / understand 7 / local-tooling 2） | 24 | 自研 |
| heygen `hyperframes` | 5 | Apache-2.0 |

逐条记录在 `catalog.yaml` 的 `origin` 字段，详见 [`NOTICE`](NOTICE)。

**本库不含**：OPC 经营层、idea-to-cash、商业判断、指标口径与实验
→ 迁到了独立库 [`opc-playbook`](https://github.com/maning636/opc-playbook)。

---

## 与插件共存

Agent 装了插件会**优先查插件**。本库据此设计：

- **插件先**：脑暴、写计划、TDD、调试、代码评审、并行子代理、完成前验证、
  git worktree、写技能 —— 一律先查插件，本库不重复造。
- **四类不让**：商业判断 / OPC 经营层 / idea-to-cash / 设计令牌与评审 /
  企业运营与指标口径 —— **只从本库与 `opc-playbook` 取**，插件不得接管。
- **冲突看 catalog，不看记忆**：每个技能在 `catalog.yaml` 里带
  `authority`（primary / fallback）与 `superseded_by`，先查字段再决定加载谁。

本机实测扫描到 25 个插件目录，其中与本库真实重叠的 4 个是
`superpowers`(15)、`Product-Manager-Skills`(46)、`plugin-dev`(7)、`skill-creator`(1)。
逐条对照见 `tools/plugin_overlap.json` 与 `INDEX.md` 的「插件已覆盖」一节。

---

## 相关库

| 库 | 角色 |
|---|---|
| [`opc-playbook`](https://github.com/maning636/opc-playbook) | OPC 经营层 9 阶段 + idea-to-cash 16 关 + 商业判断 |
| [`agent-workspace-spec`](https://github.com/maning636/agent-workspace-spec) | 工作区五层模型 + 分发规范（本库结构依据） |
| [`engineering-standard`](https://github.com/maning636/engineering-standard) | 交付红线 / 发布 / 软著 / TDD 与复核清单 |
| [`design-skills-playbook`](https://github.com/maning636/design-skills-playbook) | UI 级需求分析 / 设计评审 |
| `skills-meta`（本地） | 多库组合总线：catalog + compositions + pin + lock |

---

## 改库规则

`INDEX.md` / `CATALOG.md` / `catalog.yaml` / `manifest.json` **全部由脚本生成，不要手改**。

```bash
python tools/prune_curated.py        # 清理失效中文标签
python tools/regen_index.py          # INDEX.md
python tools/regen_skill_catalog.py  # catalog.yaml + 每域 catalog.yaml
python tools/regen_catalog.py        # CATALOG.md
python tools/regen_manifest.py       # manifest.json
```

- 改领域元信息 → `tools/domain_meta.json`
- 改中文名/触发词 → `tools/curated_zh.py`
- 改插件覆盖对照 → `tools/plugin_overlap.json`

---

**协议不重要的前提是——外部专家能读到。** 本库公开可读，欢迎直接读、直接提意见。
