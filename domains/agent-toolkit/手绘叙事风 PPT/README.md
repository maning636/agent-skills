# 手绘叙事风 PPT · 独立 Skill（lite 版）

> 从 pretty-skill 16 条铁律精简的 8 条最关键规则 · 桌面独立 skill 文件夹
> 完整 16 条方法论：`pretty-skills/内容创作/杂志风公众号品鉴/`（GitHub 公开）

## 文件结构

```
手绘叙事风PPT-skill/
├── SKILL.md                              # 30 分钟 PPT 交付总览
├── references/
│   └── hand-drawn-8-rules.md             # 8 条铁律速查
├── examples/
│   └── sample-case/
│       ├── content.md                     # 6 段骨架示范
│       └── images/
│           └── p2_matrix.png              # 3 类 9 款矩阵示范图
└── README.md                              # 本文件
```

## 适用场景

- 知识讲解类 PPT（公众号配图 / 教学课件）
- 工具评测类 PPT（多方案对比）
- 产品发布类 PPT（公司内部 + 客户汇报）
- 工作汇报类 PPT（月报 / 季报 / 年报）

## 30 分钟交付流程

1. 调研 30s（必问 1 个问题：听众 + 听完拿走什么）
2. 写 5 段钩子链 5min
3. 出 6-8 张图 10min（macaron 5 色循环）
4. 拼 .pptx 10min（dashiai-ppt / python-pptx）
5. 导出 5min（真实 .pptx，PowerPoint 可编辑）

## 8 条铁律速查

详见 `references/hand-drawn-8-rules.md`：

| # | 维度 | 规则 |
|---|---|---|
| 1 | 排版 | 0 emoji |
| 2 | 排版 | 1-3 句成段 |
| 3 | 排版 | 加粗整句做转折 |
| 4 | 叙事 | 5 段钩子链 |
| 5 | 叙事 | 分类 + 精炼 |
| 6 | 配图 | 多宫格配图 |
| 7 | 配图 | 主体居中靠下 |
| 8 | 配图 | 右下角小水印 |

**反例自检**：写完 1 份 PPT 跑 1 遍 · 8/8 = 杂志风 · 6-7 = 微调 · < 6 = 重做

## 示范 case

`examples/sample-case/content.md` 是 1 个 6 段骨架示范：
- 主题：AI 工具选哪个不踩雷
- 6 段：P0 封面 + P1 钩子 + P2 总纲 + P3 核心解法 + P4 案例 + P5 收束
- 配图：1 张 3 类 9 款矩阵（手绘 macaron 5 色）
- 认知锚点：3 类 × 3 款 = 9 选 1

## 工具栈

- **AI 出图**：matrix MCP（MiniMax Token plan 套餐）
- **PPT 拼装**：`dashiai-ppt` skill（1020 版式 × 12 主题）
- **备用**：`python-pptx`（手动嵌入 AI 出图）

## 量化疗效

| 阶段 | 之前 | 现在 | 倍速 |
|------|------|------|------|
| 写大纲 | 1h | 5min | 12x |
| 出图 | 4h | 10min | 24x |
| 拼 PPT | 3h | 10min | 18x |
| 改稿 | 2h | 5min | 24x |
| **总** | **10h** | **30min** | **20x** |

## 发到小红书 Skill Hub

桌面这份 `手绘叙事风PPT-skill/` 可以直接打包发到小红书创作者平台：

1. 打开 https://creator.xiaohongshu.com/new/skill-hub
2. 点击「上传 Skill」按钮
3. 选 `手绘叙事风PPT-skill/` 整个文件夹
4. 填 Skill 介绍（用 SKILL.md 的 description 字段）
5. 提交审核

## 完整 16 条铁律（升级版）

如果 8 条不够用，去看 `pretty-skills/内容创作/杂志风公众号品鉴/`（GitHub 公开）：
- 16 条完整铁律
- 4 张参考图
- 7 问自检
- PDF 讲解版

## 反模式

| 反模式 | 后果 | 正确做法 |
|---|---|---|
| 用 HTML 阅读器当 PPT | 不能编辑 = 死 PPT | 用 dashiai-ppt / python-pptx 出真实 .pptx |
| 1 张配图撑全场 | 视觉单调 | 6-8 张图 + 1 张多宫格 |
| 用 AI 默认紫色渐变 | AI 味 | 锁定 macaron 5 色 |
| emoji 满天飞 | 杂志感丢失 | 0 emoji |
| "在当今时代..." 套话开头 | AI 味标志 | "X 已经是日常了，但..." |
