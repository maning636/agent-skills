---
id: content-writing/bigtype-poster
domain: content-writing
name: bigtype-poster
description: 电商大字报宣传海报的标准做法：HTML 排版 + 本机 Chrome 无头渲染成 PNG。当用户要做宣传图/海报/电商首页图、换配色、调字体、调字号、出同系列新图时使用。不走 AI 扩散生图——文字必须 100% 准确的图一律用这个方法。
origin: local
license: 未声明
---


# 大字报海报做法（HTML → Chrome 渲染）

## 为什么用这个方法

- AI 生图写中文必错字；海报文字是卖点，**一个字都不能错**
- HTML 排版：文字 100% 准确，改文案/配色/字号 = 改文件重渲染，秒级
- 零成本，不消耗任何平台积分

## 标准流程

1. 复制现有模板改：`E:\FDE\multica-tuner\poster1.html` 或 `poster2.html`（1200×1200 成熟版式，勿从零写）
2. 按需调整（见下方"可调参数"）
3. 渲染：
   ```bash
   "/c/Program Files/Google/Chrome/Application/chrome.exe" --headless --disable-gpu \
     --hide-scrollbars --window-size=1200,1200 \
     --screenshot="输出路径.png" "file:///E:/.../海报.html"
   ```
4. **必须用 ReadMediaFile 读回 PNG 检查**：文字有无溢出/截断、上下黑条是否在画布内、字号是否协调。有溢出就调垂直预算（减 padding 或字号）重渲，改到好为止。

## 版式结构（从顶到底）

1. 顶部黑 pill 标签（品类定位）
2. 超大黑体主标题（两行，font-weight:900，120~150px）
3. 黑色圆角副题条（核心卖点一句话）
4. 特性框（半透明白底 + 4px 黑边，✓ 图标 + 特性列表/流程）
5. 三列短句（三个卖点词）
6. 白色圆角卡片（1~2 张，放数字或清单）
7. 底部黑色圆角条（行动指令/承诺）

## 可调参数（用户常调的）

- **底色**：`body background`，当前天蓝 `#35A8F0`。换颜色系列只改这一处
- **字体**：font-family 栈 `"Microsoft YaHei","PingFang SC","Noto Sans SC"`；要更粗换 Noto Sans SC Black 或思源黑体 Heavy，本地需已安装
- **字号**：主标题 `.title font-size`；副题 `.subbar`；卡片 `.card .big`。改版面大小时所有字号等比缩放
- **画布尺寸**：`--window-size` 和 `html,body` 宽高一起改（如电商主图 800×800、长图 750×N）

## 纪律

- 生成前先把每页全部文字发给用户审，审过再渲染
- 配色回避用户否过的颜色（2026-09 起：黄色系列禁用，用天蓝替代）
- 成品 PNG 和源 HTML 一起交付，HTML 是后续改稿的入口
- 数字必须真实可查（如"43 行业 / 54 组问题 / 近 200 问项"来自实际统计），不许编
