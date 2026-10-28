# graphify 命令参考

## 构建图谱

| 命令 | 说明 | 需要 API key |
|---|---|---|
| `graphify extract .` | 完整提取（代码+文档+PDF+图片）| ✅ |
| `graphify extract . --code-only` | 只解析代码（tree-sitter AST）| ❌ |
| `graphify extract . --no-cluster` | 跳过社区检测 | ❌ |
| `graphify extract . --out DIR` | 指定输出目录 | 视情况 |
| `graphify extract . --force` | 强制重新扫描 | 视情况 |
| `graphify extract . --postgres DSN` | 提取 PostgreSQL schema | ❌ |
| `graphify extract . --cargo` | 提取 Cargo.toml 依赖 | ❌ |
| `graphify extract . --global` | 合并到全局图谱 | ❌ |

## 查询图谱

| 命令 | 说明 | 参数 |
|---|---|---|
| `graphify query "<Q>"` | 自然语言查询 | `--dfs` `--budget N` `--context C` |
| `graphify path "A" "B"` | 最短路径 | `--graph PATH` |
| `graphify explain "X"` | 概念解释 | `--graph PATH` |
| `graphify affected "X"` | 反向遍历（影响分析）| `--relation R` `--depth N` |
| `graphify god-nodes` | 最连接节点 | `--top N` `--json` |

## 导出

| 命令 | 产出格式 | 说明 |
|---|---|---|
| `graphify export html` | HTML | 交互式图谱 |
| `graphify export svg` | SVG | 静态图（需 `[svg]` 可选依赖）|
| `graphify export callflow-html` | HTML | Mermaid 调用流程图 |
| `graphify export obsidian` | Markdown + Canvas | Obsidian 笔记库 |
| `graphify export wiki` | Markdown | Wiki 文章 |
| `graphify export graphml` | GraphML | 通用图格式 |
| `graphify export neo4j` | Cypher | Neo4j 推入 |
| `graphify export falkordb` | Cypher | FalkorDB 推入 |
| `graphify tree` | HTML | D3 可折叠树 |

## 维护

| 命令 | 说明 |
|---|---|
| `graphify update .` | 增量更新（不调 LLM）|
| `graphify update . --force` | 强制覆盖 |
| `graphify watch .` | 文件监控自动重建 |
| `graphify check-update .` | 检查是否需要更新 |
| `graphify cluster-only .` | 重新聚类 |
| `graphify label .` | 重新标注社区 |

## 服务

| 命令 | 说明 |
|---|---|
| `graphify serve graph.json` | MCP server（stdio）|
| `graphify serve-http graph.json` | HTTP server |
| `graphify global add graph.json` | 添加到全局图谱 |
| `graphify global list` | 列出全局图谱项目 |
| `graphify global remove TAG` | 从全局图谱移除 |
| `graphify merge-graphs g1 g2` | 合并多个图谱 |

## 反馈

| 命令 | 说明 |
|---|---|
| `graphify save-result` | 保存 Q&A 用于反馈 |
| `graphify reflect` | 聚合反馈生成经验文档 |

## 外部内容

| 命令 | 说明 |
|---|---|
| `graphify add URL` | 抓取 URL 加入图谱 |
| `graphify clone GITHUB_URL` | 克隆仓库 |

## 平台安装

| 命令 | 平台 |
|---|---|
| `graphify install` | 自动检测平台 |
| `graphify claude install` | Claude Code |
| `graphify cursor install` | Cursor |
| `graphify codex install` | Codex |
| `graphify gemini install` | Gemini CLI |
| `graphify aider install` | Aider |
| `graphify vscode install` | VS Code Copilot |
| `graphify opencode install` | OpenCode |
| `graphify trae install` | Trae |
