---
id: content-writing/graphify
domain: content-writing
name: graphify
description: 代码知识图谱引擎。当用户想分析项目架构、查询模块关联、查找关键概念、生成架构图、导出图谱为各种格式时使用。graphify 用 tree-sitter AST 本地确定性解析代码（40+ 语言，零 LLM 成本），输出可交互的知识图谱、分析报告和多格式导出。支持 MCP Server 接入 Agent、HTTP Server 网络访问、文件监控自动重建。
version: 1.0.0
origin: local
license: 未声明
---


# graphify — 代码知识图谱引擎

## 何时使用

- 用户问"这个项目里哪个模块最复杂/最重要"
- 用户问"X 和 Y 之间有什么关联"
- 用户问"这个项目的架构是什么样的"
- 用户要"生成架构图""导出图谱""看看依赖关系"
- 用户要"把这个项目的代码变成知识图谱"
- 用户要把图谱接入 AI Agent（MCP Server）

## 前置条件

1. graphify 已安装（`uv tool install graphifyy`）
2. 验证：`graphify --version`
3. 代码分析**不需要 API key**（tree-sitter 本地 AST 解析）
4. 文档/PDF/图片分析需要 LLM API key（见"配置 LLM"）

---

## 核心工作流

### 第一步：构建图谱

```bash
# 只解析代码（推荐，零成本，最常用）
graphify extract . --code-only

# 解析代码 + 文档 + PDF + 图片（需要 API key）
graphify extract .

# 指定输出目录
graphify extract /path/to/project --out /path/to/output
```

**产出物：**

```
<output>/graphify-out/
├── graph.json          # 知识图谱数据（机器可读，核心）
├── GRAPH_REPORT.md     # 分析报告（人可读）
├── graph.html          # 交互式图谱（浏览器打开）
├── .graphify_analysis.json  # 分析结果
└── .graphify_labels.json    # 社区标签
```

### 第二步：查询图谱

```bash
# 自然语言查询
graphify query "APIRouter 被哪些模块使用？"

# 查找两个概念之间的最短路径
graphify path "FastAPI" "ModelField"

# 解释一个概念
graphify explain "APIRouter"

# 查找受某变更影响的节点（反向遍历）
graphify affected "AuthMiddleware"

# 列出最连接的节点（架构枢纽）
graphify god-nodes --top 10
graphify god-nodes --json

# BFS 遍历（可控制预算）
graphify query "数据库连接如何管理？" --budget 3000

# DFS 遍历
graphify query "事件循环在哪里被阻塞？" --dfs
```

### 第三步：导出图谱

```bash
# HTML（交互式，浏览器打开）
graphify export html

# SVG（静态，可嵌入文档）
graphify export svg

# Mermaid 调用流程图
graphify export callflow-html --lang zh-CN

# Obsidian 笔记库
graphify export obsidian --dir ./obsidian-graph

# Wiki Markdown
graphify export wiki

# GraphML（通用图格式）
graphify export graphml

# Neo4j Cypher
graphify export neo4j

# FalkorDB Cypher
graphify export falkordb

# D3 可折叠树
graphify tree --output graphify-out/GRAPH_TREE.html
```

---

## 查询图谱（直接读 JSON）

当用户问图谱相关问题时，Agent 可以直接读 `graphify-out/graph.json`：

```python
import json

with open("graphify-out/graph.json") as f:
    graph = json.load(f)

# 结构
nodes = graph["nodes"]   # [{id, label, source_file, source_location, ...}]
edges = graph["edges"]   # [{source, target, relation, confidence, ...}]
```

**节点字段：**
| 字段 | 说明 |
|---|---|
| `id` | 唯一标识 |
| `label` | 人类可读名称 |
| `source_file` | 源文件路径 |
| `source_location` | 行号（如 L42）|

**边字段：**
| 字段 | 说明 |
|---|---|
| `source` | 源节点 id |
| `target` | 目标节点 id |
| `relation` | calls / imports / uses / 等 |
| `confidence` | EXTRACTED / INFERRED / AMBIGUOUS |

**置信度标签：**
| 标签 | 含义 | 可信度 |
|---|---|---|
| `EXTRACTED` | 源码中明确写出 | ✅ 高 |
| `INFERRED` | 合理推断 | ⚠️ 中 |
| `AMBIGUOUS` | 不确定 | ❓ 低 |

---

## 进阶功能

### 增量更新

```bash
# 代码变更后更新图谱（不调 LLM）
graphify update .

# 强制覆盖（删除代码后）
graphify update . --force
```

### 文件监控

```bash
# 监控目录，代码变更自动重建
graphify watch .
```

### MCP Server（接入 Agent）

```bash
# 启动 MCP server（stdio 模式）
graphify serve graphify-out/graph.json

# 启动 HTTP server
graphify serve-http graphify-out/graph.json --port 8080
```

### 全局图谱

```bash
# 添加项目到全局图谱
graphify global add graphify-out/graph.json --as my-project

# 查看全局图谱中的所有项目
graphify global list

# 从全局图谱移除
graphify global remove my-project

# 查看全局图谱路径
graphify global path
```

### 跨项目合并

```bash
# 合并两个项目的图谱
graphify merge-graphs project-a/graphify-out/graph.json project-b/graphify-out/graph.json --out merged.json
```

### 添加外部内容

```bash
# 抓取 URL 加入图谱
graphify add https://example.com/docs --author "作者名"
```

### 反馈循环

```bash
# 保存查询结果用于反馈
graphify save-result --question "X 和 Y 关联" --answer "..." --nodes node1 node2

# 聚合反馈生成经验文档
graphify reflect
```

---

## 配置 LLM（可选）

代码分析不需要 LLM。只有文档/PDF/图片的语义分析需要：

```bash
# 设置环境变量（选一个）
export GEMINI_API_KEY="..."      # Gemini
export OPENAI_API_KEY="..."      # OpenAI
export ANTHROPIC_API_KEY="..."   # Claude
export DEEPSEEK_API_KEY="..."    # DeepSeek
export MOONSHOT_API_KEY="..."    # Kimi

# 或指定本地模型（Ollama）
export OPENAI_BASE_URL="http://localhost:11434/v1"
export OPENAI_MODEL="llama3"
```

**后端选择：**
| 后端 | 环境变量 | 模型 |
|---|---|---|
| Gemini | GEMINI_API_KEY / GOOGLE_API_KEY | 自动 |
| OpenAI | OPENAI_API_KEY | 自动 |
| Claude | ANTHROPIC_API_KEY | 自动 |
| DeepSeek | DEEPSEEK_API_KEY | 自动 |
| Kimi | MOONSHOT_API_KEY | 自动 |
| Ollama | OPENAI_BASE_URL + OPENAI_MODEL | 本地 |

---

## 可选功能安装

```bash
# SVG 导出（matplotlib + numpy）
uv tool install "graphifyy[svg]"

# 视频/音频（faster-whisper + yt-dlp）
uv tool install "graphifyy[video]"

# 全部功能
uv tool install "graphifyy[all]"
```

---

## 反模式（禁止）

1. **不要在没有图谱的情况下回答架构问题**——先跑 `graphify extract . --code-only`
2. **不要把 INFERRED 边当 EXTRACTED 边**——置信度标签是事实，不是建议
3. **不要用 `graphify query` 代替直接读 JSON**——简单查询直接读 JSON 更快
4. **不要在代码分析时设 API key**——`--code-only` 零成本，不需要 LLM
5. **不要忽略 AMBIGUOUS 边**——这些是图谱最诚实的部分，标记它们供人工审查
6. **不要跳过 god-nodes**——最连接的节点是架构枢纽，总是先查这个
7. **不要合并不相关的图谱**——`merge-graphs` 会保留社区边界，但合并前确认语义一致
8. **不要在 CI 里跑完整提取**——用 `--code-only` 或 `update` 增量更新
9. **不要覆盖 graph.json**——`update --force` 只在删除代码后使用，否则会丢失数据
10. **不要忽略 AMBIGUOUS 边**——这是图谱最诚实的部分，标记它们供人工审查

---

## 自检清单

每次使用 graphify 后，检查：

| # | 检查项 | 通过标准 |
|---|---|---|
| 1 | 图谱已构建 | `graphify-out/graph.json` 存在且非空 |
| 2 | 置信度标签 | 边的 confidence 字段都是 EXTRACTED/INFERRED/AMBIGUOUS |
| 3 | 节点来源 | 每个节点有 source_file 和 source_location |
| 4 | 报告已生成 | `GRAPH_REPORT.md` 存在 |
| 5 | 可视化可用 | `graph.html` 可在浏览器打开 |
| 6 | 查询验证 | 用 `graphify query` 验证一个已知问题 |
| 7 | 导出正确 | 目标格式文件存在且非空 |
| 8 | 增量更新 | 代码变更后 `graphify update .` 正常 |
| 9 | MCP 可用 | `graphify serve` 可启动（如需要）|
| 10 | 无孤立节点 | 检查是否有 source_file 为空的节点 |

---

## 常见问题

### Q: graphify 命令找不到
```bash
# 验证安装
graphify --version

# 如果找不到，重新安装
uv tool install graphifyy

# 确保 uv 的 bin 目录在 PATH 中
export PATH="$HOME/.local/bin:$PATH"
```

### Q: 代码分析报错 "no LLM API key found"
```bash
# 用 --code-only 跳过文档分析
graphify extract . --code-only
```

### Q: 图谱太大，graph.html 打不开
```bash
# 跳过可视化，只生成 JSON 和报告
graphify extract . --code-only --no-cluster

# 或限制节点数
graphify export html --node-limit 1000
```

### Q: 中文标签乱码
```bash
# 确保终端编码为 UTF-8
chcp 65001

# 或指定输出语言
graphify export callflow-html --lang zh-CN
```

### Q: 如何在 CI 中使用
```bash
# CI 里用 --code-only（零成本）
graphify extract . --code-only

# 增量更新
graphify update .

# 检查是否需要更新
graphify check-update .
```

---

## 与其他 Skill 的组合

### + interaction-prd

```
场景：新产品 PRD + 现有代码分析

1. graphify 分析现有代码
   graphify extract . --code-only
   → 产出 graph.json + GRAPH_REPORT.md

2. interaction-prd 写 PRD
   → 引用 graphify 的分析结果作为"实测"证据
   → 走 9 步工作流生成 PRD
```

### + 你的工作台

```
场景：工作台架构分析

1. graphify 分析工作台代码
   cd D:\工作台\content-automation-platform
   graphify extract . --code-only

2. Agent 查询图谱
   graphify god-nodes --top 10
   → 找到最复杂的模块

3. 生成架构图
   graphify export callflow-html --lang zh-CN
   → 生成 Mermaid 调用流程图

4. 导出为 Obsidian
   graphify export obsidian
   → 每社区一篇 Markdown 笔记
```

### + MCPJungle

```
场景：图谱接入 Agent 生态

1. 构建图谱
   graphify extract . --code-only

2. 启动 MCP server
   graphify serve graphify-out/graph.json

3. 注册到 MCPJungle（8080 端口）
   → 任何 Agent 都可以通过 MCP 查询图谱
```

---

## 基准数据

| Benchmark | Metric | graphify | 对比 |
|---|---|---|---|
| LOCOMO (n=300) | recall@10 | **0.497** | mem0 0.048, supermemory 0.149 |
| LOCOMO (n=300) | QA accuracy | 45.3% | supermemory 49.7%, mem0 27.3% |
| LongMemEval-S (n=50) | QA accuracy | **76%** | 与 dense RAG 持平 |
| 代码解析 | LLM 成本 | **0** | 大多数系统按 token 计费 |

---

## 支持的语言

~40 种，通过 tree-sitter AST 解析：

Python · TypeScript · JavaScript · Go · Rust · Java · C · C++ · C# · PHP · Ruby · Swift · Kotlin · Scala · Erlang · Elixir · Haskell · Lua · R · MATLAB · Racket · Julia · V · Bash · PowerShell · Verilog · Zig · Fortran · Groovy · JSON · YAML · TOML · Markdown · HTML · SQL · Protobuf · GraphQL · 等
