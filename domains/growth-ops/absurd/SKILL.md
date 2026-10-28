---
id: growth-ops/absurd
domain: growth-ops
name: absurd
description: "Absurd 0.4.0 durable task execution（PostgreSQL-native）。spawn/claim/emit_event/cancel/retry 长时间运行的 agent 任务，崩溃后从 checkpoint 恢复，awaitEvent/sleep 事件驱动协调，exactly-once 语义。触发词：absurd、durable workflow、spawn task、checkpoint、resume task、absurd event、长任务、持久化任务、agent 调度、durable execution、Postgres 任务队列。也适用于用户说『跑一个长任务』、『任务挂掉恢复』、『等事件触发』的场景。"
version: 0.4.0
metadata: 
origin: 本机自研
license: 见来源
---


# Absurd Skill (v0.4.0)

PostgreSQL-native durable task execution via `absurd-sdk` (PyPI)。

让 agent 任务**崩溃可恢复**、**事件可唤醒**、**重试不丢步**。底层是 Postgres stored procedures,不需要额外的 message broker / scheduler。

## 健康检查（永远先跑这个）

```bash
bash C:/Users/maning/.agents/skills/absurd/absurd_diagnostics.sh
```

返回 `status: ok` 且 `queue_count > 0` 才能继续。

如果返回 `error` → 检查 Postgres 服务 `postgresql-x64-16` 是否 RUNNING,且 `absurd_db` 数据库已初始化。

## 数据库要求

- `ABSURD_DATABASE_URL` 环境变量必须设置,例如:
  ```
  postgresql://postgres:postgres@127.0.0.1:5432/absurd_db
  ```
- Schema 已初始化(11 张表在 `absurd` schema:`t_/r_/c_/w_/e_` × 2 queues + `queues`)
- SDK `create_queue()` 会自动建队列表

## 工具列表（8 个 wrapper）

每个脚本输出 JSON 到 stdout。在 Pi shell 中直接调用,或通过 MCP server `absurd-fix` 调用。

| 工具 | Args | 默认 queue | 说明 |
|------|------|-----------|------|
| `absurd_diagnostics` | — | — | 健康检查(v2)。返回 `task_table_ready` / `event_table_ready`。**永远先跑**。任一 false → `status=degraded` |
| `absurd_spawn` | `--task-name <name>` (必填)<br>`--params <json>`<br>`--queue <name>` (默认 `agent-tasks`)<br>`--max-attempts <int>` (默认 3) | `agent-tasks` | 派发任务,返回 task_id/run_id/attempt |
| `absurd_list_tasks` | `--queue <name>` (默认 `agent-tasks`)<br>`--limit <int>` (默认 10) | `agent-tasks` | 列出 pending/running tasks,watchdog 用 |
| `absurd_emit_event` | `--event <name>` (必填)<br>`--payload <json>`<br>`--queue <name>` | `agent-tasks` | 唤醒 suspend 在 `awaitEvent(name)` 上的任务。**多 agent 协调用** |
| `absurd_retry` | `--task-id <uuid>` (必填)<br>`--queue <name>`<br>`--spawn-new` | `agent-tasks` | 重试 failed task。`--spawn-new` 起新 attempt |
| `absurd_cancel` | `--task-id <uuid>` (必填)<br>`--queue <name>` | `agent-tasks` | 标记 cancelled,worker 应中断 |
| `absurd_fetch_result` | `--task-id <uuid>` (必填)<br>`--queue <name>` | `agent-tasks` | 读最终结果。`state` ∈ `completed/failed/cancelled/suspended/running` |
| `absurd_list_queues` | — | — | 列出所有 queue |

## 调用示例

```bash
# 1. 派发任务
bash C:/Users/maning/.agents/skills/absurd/absurd_spawn.sh \
  --task-name architect-design \
  --params '{"goal": "设计 token 认证"}' \
  --queue agent-tasks

# → 返回 {"task_id": "019ec...", "run_id": "...", "attempt": 1, "status": "spawned"}

# 2. 看进度
bash C:/Users/maning/.agents/skills/absurd/absurd_fetch_result.sh \
  --task-id <task_id>

# 3. 唤醒 suspend 任务（多 agent hand-off）
bash C:/Users/maning/.agents/skills/absurd/absurd_emit_event.sh \
  --event "design.reviewed:project-123" \
  --payload '{"verdict": "approved"}' \
  --queue agent-tasks
```

## 核心使用模式

### 1. 长任务派发 + 监控
```bash
TASK_ID=$(bash absurd_spawn.sh --task-name long-job ... | jq -r .task_id)
# watchdog 轮询
bash absurd_fetch_result.sh --task-id $TASK_ID
```

### 2. 多 Agent 协作(核心场景)
Agent A 跑完 → emit event → Agent B 恢复:
```bash
# Agent A 完成阶段
bash absurd_emit_event.sh \
  --event "design.reviewed:project-123" \
  --payload '{"verdict": "approved"}'
# Agent B (suspend 在 ctx.awaitEvent("design.reviewed:project-123")) 自动醒来
```

### 3. Watchdog(检测 idle agent)
```bash
bash absurd_list_tasks.sh --queue agent-tasks --limit 50
# 看: status=running 超过 15 分钟,或 status=queued 但没 worker
```

### 4. 崩溃恢复
Absurd 自动从上一个 checkpoint 恢复。手动恢复:
```bash
bash absurd_retry.sh --task-id <uuid>
# 起新 attempt:
bash absurd_retry.sh --task-id <uuid> --spawn-new
```

## 为什么是 Absurd(不是 cron / RabbitMQ)

- **Checkpoint 重试**:每个 `ctx.step()` 持久化返回值,重试时不重复执行已完成步骤
- **事件驱动协调**:`awaitEvent()` 挂起任务到命名事件触发,first-write-wins 无竞态
- **多语言 worker**:Python/TypeScript/Go SDK 都对同一份 Postgres schema 说话
- **零额外服务**:没有 message broker、没有 scheduler,只有 Postgres stored procedures

## 部署位置

| 用途 | 路径 |
|------|------|
| **真源**(本仓库) | `C:/Users/maning/.agents/skills/absurd/` |
| **Pi symlink** | `C:/Users/maning/.pi/agent/skills/absurd` → 真源 |
| **独立 MCP server**(可选) | `D:/work/absurd-fix-mcp/server.py` (mcpjungle 已 deregister) |
| **独立 MCP 配置片段** | `D:/研究/mcp-configs-absurd-standalone.json` |

## 故障排查

如果 wrapper 脚本报错:

| 错误 | 原因 | 修法 |
|------|------|------|
| `connection refused` | PG 没启动 | `net start postgresql-x64-16` |
| `database "absurd_db" does not exist` | 没建库 | `createdb -U postgres absurd_db` |
| `relation "absurd.t_<queue>" does not exist` | 队列没初始化 | SDK `create_queue("xxx")` 自动建 |
| `Task is not currently failed` | retry 只能重试 failed | 用 `--spawn-new` 起新 attempt,或先 cancel |
| `queue not found` | queue_name 拼错 | `bash absurd_list_queues.sh` 查实际名 |

## 变更日志

| 日期 | 修改 |
|------|------|
| 2026-06-15 | 初版部署 — 8 个 wrapper 脚本 + Pi symlink + 端到端验证通过 |