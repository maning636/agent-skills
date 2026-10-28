---
id: content-writing/prism-content
domain: content-writing
name: prism-content
description: "创作角色产出回流规范：把成品稿件/图片/视频交付到本机 Prism 平台（素材入库或 Easel 稿件桥），并触发发布官走人工确认分发。任何创作角色产出成品后必须按本技能交付。"
version: 1.0.0
author: Prism Ops
origin: local
license: 未声明
---


# 创作产出回流 Prism

创作角色（内容创作官/微信运营员/制片等）产出成品后的**标准交付动作**。

## 交付前检查

1. 成品文件完整（图片成套、视频成片、文本定稿）
2. 元数据齐全：标题、平台、标签、摘要

## 方式 A：入库素材库（默认）

```bash
curl -sS -X POST "http://127.0.0.1:7000/api/v1/files/upload-save" \
  -F "file=@成品路径" \
  -F "filename=稿件标题-平台.ext" \
  -F "group=monica:<issue号或项目名>" \
  -F "note={\"title\":\"...\",\"platform\":\"...\",\"tags\":[\"...\"]}"
```

返回 `data.file_id` 即素材 ID，记入汇报。

## 方式 B：Easel 稿件桥（适合多文件成套稿件）

把成品+`.easel.json` 元数据写入 `D:\工作台\Easel\outputs\<项目名>\`：

```json
{
  "title": "稿件标题",
  "summary": "一句话摘要",
  "platform": "xiaohongshu",
  "kind": "card",
  "status": "draft",
  "tags": ["标签"],
  "cover": "封面文件名",
  "deliverables": ["文件1", "文件2"]
}
```

写入后稿件自动出现在 Prism「Easel 稿件箱」页，可一键导入建投放计划。

## 汇报与发布流转

交付完成后按以下格式汇报：

```
📤 已回流 Prism：<稿件标题>
- 方式：素材库（file_id: N）/ Easel 稿件桥（项目: xxx）
- 明细：http://localhost:3000/materials
- 下一步：@发布官 安排分发（需人工确认）
```

## 铁律

- 回流是创作角色的终点，**发布永远由发布官执行**（人工确认后才动调度器）
- 不要直接调用 campaigns/create——那是发布官的职责边界
