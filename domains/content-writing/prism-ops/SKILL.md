---
id: content-writing/prism-ops
domain: content-writing
name: prism-ops
description: "操作本机 Prism 内容分发平台：素材入库、创建矩阵投放计划、控制发布进度、查询任务与效果数据。当用户要求发布内容、上传素材、建投放计划、查发布结果/数据时使用。发布前必须获得人工确认。"
version: 1.0.0
author: Prism Ops
origin: local
license: 未声明
---


# Prism 平台操作

本机运行的 Prism 内容分发平台（矩阵发布控制台）。所有接口在本机直接可调，无需认证。

## 平台地址

- API Base: `http://127.0.0.1:7000`
- Web UI: `http://localhost:3000`

## 铁律：人工确认后才发布

- 创建投放计划（campaigns/create）**之前**，必须在对话中获得用户的明确确认
- `execute_now=true`（立即生成发布任务）仅在用户明确说"发布/执行"或对应任务已在 Monica 标记为 Ready to Publish 时使用
- 仅查询类操作（素材列表、进度、数据）无需确认

## 1. 素材入库

```bash
curl -sS -X POST "http://127.0.0.1:7000/api/v1/files/upload-save" \
  -F "file=@/path/to/video.mp4" \
  -F "filename=显示名称.mp4" \
  -F "group=来源标识" \
  -F "note=备注信息"
```

- 返回 `data` 中包含 `file_id`（后续建投放计划用 material_ids=[file_id]）
- 单文件上限 160MB；支持视频 mp4/mov/avi/mkv、图片、文档
- `group` 建议写来源（如 `monica:MUL-42`），便于溯源

## 2. 查询素材库

```bash
curl -sS "http://127.0.0.1:7000/api/v1/files/?page=1&page_size=20"
```

返回条目含 `id` / `filename` / `group_name` / `filesize`。

## 3. 创建投放计划

```bash
curl -sS -X POST "http://127.0.0.1:7000/api/v1/campaigns/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "计划名称",
    "platforms": ["douyin", "xiaohongshu"],
    "account_ids": ["账号ID列表"],
    "material_ids": [101, 102],
    "schedule_type": "immediate",
    "execute_now": true,
    "remark": "备注"
  }'
```

- `platforms` 可选值: douyin / kuaishou / xiaohongshu / bilibili / channels / tiktok / youtube
- `account_ids`: 必须是平台真实存在的账号（先查账号，见 §7）
- `material_ids`: 素材 file_id 数组
- `schedule_type`: immediate（立即）/ range（区间）/ daily（每日定量）
- `execute_now`: true=立即生成发布任务并进入调度队列；false=仅存为草稿
- 返回 `result.campaign_id` 与 `result.tasks_created`

## 4. 查询计划与真实进度

```bash
curl -sS "http://127.0.0.1:7000/api/v1/campaigns/list"
```

每个计划带 `progress`（0-100 真实执行进度）与 `task_stats`（各状态任务数：
finished/failed/running/pending/retry/need_verification）。

## 5. 计划控制

```bash
# 暂停 / 恢复 / 执行 / 删除
curl -sS -X POST "http://127.0.0.1:7000/api/v1/campaigns/{id}/pause"
curl -sS -X POST "http://127.0.0.1:7000/api/v1/campaigns/{id}/resume"
curl -sS -X POST "http://127.0.0.1:7000/api/v1/campaigns/{id}/execute"
curl -sS -X DELETE "http://127.0.0.1:7000/api/v1/campaigns/{id}"
```

## 6. 任务与效果数据

```bash
# 任务列表与统计
curl -sS "http://127.0.0.1:7000/api/v1/tasks/stats"
curl -sS "http://127.0.0.1:7000/api/v1/tasks/list?page=1&page_size=20"
```

效果/播放/互动数据在数据中心模块（/analytics 前端页，API `/api/v1/analytics/*`）。

## 7. 查询可用账号

```bash
curl -sS "http://127.0.0.1:7000/api/v1/accounts/?limit=100"
```

返回条目含 `account_id` / `platform` / `nickname`。创建计划前先按 `platform` 筛选。

## 8. Easel 稿件桥（可选）

Easel 创作工作台的稿件可直接导入：

```bash
# 稿件列表（title/platform/tags/cover）
curl -sS "http://127.0.0.1:7000/api/v1/easel/drafts"
# 导入稿件成品到素材库，返回 material_ids
curl -sS -X POST "http://127.0.0.1:7000/api/v1/easel/drafts/{project}/import"
```

## 9. 向 Monica 回帖的汇报格式

任务完成后按此格式汇报（便于团队统一阅读）：

```
✅ 已完成：<做了什么>
- 素材：file_id <列表>
- 投放计划：#<campaign_id>（<平台列表>，N 个任务）
- 进度：<progress>%（finished X / total Y）
- 明细：http://localhost:3000/campaigns
```

失败时：说明失败环节、错误信息、建议动作；不要重试发布类操作（先问人）。
