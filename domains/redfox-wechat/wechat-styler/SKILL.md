---
id: redfox-wechat/wechat-styler
domain: redfox-wechat
name: wechat-styler
description: 将 Markdown 文章转换为微信公众号可用的内联样式 HTML，默认使用 kami 纸感主题，支持 kami、magazine-ink、magazine-indigo、magazine-forest、elegant、modern、minimal 多主题切换和字体、字号、强调色、背景色、输出路径等参数配置。用于公众号排版、文章 HTML 生成、替代不稳定外部排版服务，尤其适合把本 vault 内文章转成可复制到微信公众号编辑器的格式。
version: 1.5.0
origin: redfox-data/redfox-community
license: MIT
---


# WeChat Styler - 公众号排版工具

将 Markdown 文章转换为优雅的公众号 HTML 格式，支持多主题切换。

## 效果预览

使用 2026-06-30 最近抓取的真实 WorkBuddy 文档节选生成，左侧为原始 Markdown，右侧为 `zhijian` 主题输出。

![WeChat Styler 左右并列效果预览](https://obsidian-1344509300.cos.ap-beijing.myqcloud.com/obsidian/img/wechat-styler-before-after-recent.png)

## 使用方式

```bash
# 基础用法（使用默认主题）
/wechat-styler path/to/article.md

# 指定主题
/wechat-styler path/to/article.md --theme kami
/wechat-styler path/to/article.md --theme magazine-ink

# 批量转换（支持 glob 模式）
/wechat-styler "articles/*.md" --theme kami
/wechat-styler "01_项目/内容创作/**/*.md" --theme magazine-ink

# 自定义参数
/wechat-styler path/to/article.md --theme kami --font-size 17 --accent-color "#1B365D"

# 输出到指定路径（单文件）
/wechat-styler path/to/article.md --output path/to/output.html
```

## 可用主题

### 0. zhijian（智见AI 品牌主题）- 默认主题

**特点：**
- 基于 DESIGN.md 品牌系统，暖纸感 × 顾问可信度
- 纸感背景 `#F5F4ED`，深暖陶行动色 `#B85235`，墨蓝结构色 `#1B365D`
- 三层字体策略：标题楷体（品牌感）、正文宋体（可读性）、UI 黑体（功能性）
- H2 左侧暖陶竖线，H3 墨蓝色，引用块 Human Accent 左线
- 代码块暖黑底 12px 圆角，行内代码墨蓝色浅蓝底
- 加粗和链接使用 `#A04A2E`（WCAG AA 安全暖色）
- 分隔线使用暖陶色短线居中

**适用场景：** 所有智见AI品牌内容 — 公众号文章、培训讲义、课程内容、方法论分享、AI 落地案例

**参数：**
```yaml
font_family_cn: 'Source Han Serif SC','Noto Serif CJK SC','Songti SC',Georgia,serif
font_family_en: 'Georgia','Source Serif 4','Charter','Times New Roman',serif
font_size: 17
line_height: 1.58
accent_color: '#B85235'
accent_secondary: '#1B365D'
background_color: '#F5F4ED'
surface_color: '#FAF9F5'
text_color: '#141413'
heading_font: 'TsangerJinKai02','Source Han Serif SC','Noto Serif CJK SC','Songti SC',Georgia,serif
ui_font: 'Source Han Sans SC','Noto Sans CJK SC','PingFang SC',-apple-system,sans-serif
code_font: 'JetBrains Mono','SF Mono','Fira Code',Consolas,Monaco,'Source Han Serif SC',monospace
code_bg: '#30302E'
code_color: '#F5F4ED'
```

### 1. kami（紙感编辑排版）

**特点：**
- warm parchment 纸感背景：`#f5f4ed`
- ink-blue 单一强调色：`#1B365D`
- 中文标题使用衬线/楷体栈，正文使用稳定无衬线栈
- 温暖灰阶，不使用冷灰和纯白大底
- 标题左侧蓝色竖线、solid tag 背景、克制引用块
- 所有背景色使用 solid hex，并在外层、内容层、文本层重复声明，降低粘贴到公众号后背景丢失风险

**适用场景：** 公众号深度文章、商业分析、课程内容、正式说明文

**参数：**
```yaml
font_family_cn: 'Inter','TsangerJinKai02','Source Han Sans SC','Noto Sans CJK SC','PingFang SC','Microsoft YaHei',Arial,sans-serif
font_family_en: 'Newsreader','Source Serif 4','Source Serif Pro','Charter',Georgia,'Times New Roman',serif
font_size: 16
line_height: 1.55
accent_color: '#1B365D'
background_color: '#f5f4ed'
surface_color: '#faf9f5'
text_color: '#141413'
secondary_color: '#5e5d59'
heading_font: 'TsangerJinKai02','Source Han Serif SC','Noto Serif CJK SC','Songti SC','STSong',Georgia,serif
code_font: 'JetBrains Mono','SF Mono','Fira Code',Consolas,Monaco,'TsangerJinKai02','Source Han Serif SC',monospace
```

### 2. magazine 系列（电子杂志 × 电子墨水）

从 `magazine-web-ppt` 迁移来的预设，保留 `ink / paper / tint` 的杂志色彩关系，同时改造成微信公众号安全 HTML：不使用 `rgba()`，所有背景色均为 solid hex。

| 主题 | 命令 | 变体 | 字体 / 版式人格 |
|------|------|------|------------------|
| 墨水经典 | `--theme magazine-ink` | `ink-classic` | 无衬线正文 + 衬线标题，细 rule、dash list、pull quote，通用杂志内页 |
| 靛蓝瓷 | `--theme magazine-indigo` | `indigo-research` | Inter/SF Pro 正文 + Source Serif 标题，左侧研究栏、note quote、技术代码块 |
| 森林墨 | `--theme magazine-forest` | `forest-fieldnote` | 楷体/宋体正文 + 非虚构标题，居中标题、field note 引用、自然图片说明 |

**共同特点：**
- 每个主题都有独立字体栈、字号、行距、段距、标题结构、列表 marker、引用块、代码块和图片说明。
- 分隔以留白、短淡线和局部标识为主；不会在每个章节之间自动插入整宽实线。
- 五个主题共享 `magazine-editorial` renderer 入口，但通过 `magazine_variant` 走不同结构分支，不只是替换颜色。
- 所有背景色都使用 solid hex，并在区块与文本 span 上重复声明 `background-color`，降低复制到公众号编辑器后背景色丢失的概率。
- 图片自身带 `margin:0 auto` 居中兜底，避免公众号编辑器复制后改写图片宽度导致图片靠左。
- 版式保留杂志感，但输出仍完全内联，可直接复制到公众号编辑器。

### 3. elegant（优雅复古）

**特点：**
- 中文：方正书宋（FZShuSong-Z01）
- 英文：Garamond
- 整体淡灰色背景
- 红色强调色系统
- 衬线标题 + 等宽代码

**适用场景：** 商业案例、深度分析、知识分享

**参数：**
```yaml
font_family_cn: 'FZShuSong-Z01','Songti SC',STSong,serif
font_family_en: 'Garamond',serif
font_size: 16
line_height: 1.9
accent_color: '#cf4436'
background_color: '#f7f6f1'
heading_font: 'Noto Serif SC','Songti SC',STSong,Georgia,serif
code_font: 'JetBrains Mono','SF Mono',Menlo,Consolas,monospace
```

### 4. modern（现代简约）

**特点：**
- 无衬线字体
- 纯白背景
- 蓝色强调色
- 清晰现代

**适用场景：** 科技产品、教程、快讯

**参数：**
```yaml
font_family_cn: 'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif
font_family_en: 'SF Pro Display','Helvetica Neue',sans-serif
font_size: 16
line_height: 1.8
accent_color: '#007aff'
background_color: '#ffffff'
heading_font: 'PingFang SC','Hiragino Sans GB',sans-serif
code_font: 'SF Mono',Menlo,Consolas,monospace
```

### 5. minimal（极简主义）

**特点：**
- 极简黑白
- 大量留白
- 灰色调
- 克制优雅

**适用场景：** 哲学思考、个人随笔、艺术评论

**参数：**
```yaml
font_family_cn: 'Noto Sans SC','PingFang SC',sans-serif
font_family_en: 'Inter','Helvetica Neue',sans-serif
font_size: 15
line_height: 2.0
accent_color: '#333333'
background_color: '#fafafa'
heading_font: 'Noto Sans SC',sans-serif
code_font: 'JetBrains Mono',monospace
```

## Renderer Presets

主题不只换颜色。每个主题绑定一个 Markdown 渲染人格，负责标题、正文、引用、列表、代码、图片说明的结构、字号、行高、间距和字重。

| Preset | 绑定主题 | 版式语气 |
|--------|----------|----------|
| `zhijian-warm-paper` | `zhijian` | 品牌讲义：暖陶竖线标题、墨蓝三级标题、Human Accent 引用、暖黑代码块 |
| `kami-document` | `kami` | 纸感文档：正式、克制、标题左侧 ink-blue 竖线 |
| `magazine-editorial` | `magazine-ink` / `magazine-indigo` / `magazine-forest` | 电子杂志家族：通过 `magazine_variant` 分别呈现 classic / research / fieldnote 三种版式 |
| `elegant-essay` | `elegant` | 复古长文：居中标题、舒展行距、摘录式引用 |
| `modern-technical` | `modern` | 现代教程：无衬线层级、提示卡片、技术代码块 |
| `minimal-notes` | `minimal` | 极简笔记：低装饰、大留白、细线引用 |

**公众号兼容硬规则：** 所有 preset 输出均为 inline style；背景色使用 solid hex；外层 section、内容 section、文本 span 会重复声明 `background-color`。

## 主题参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--theme` | 主题名称 | `zhijian` |
| `--font-size` | 正文字号（px） | `17` |
| `--line-height` | 行高 | `1.58` |
| `--accent-color` | 强调色（标题、链接） | `#B85235` |
| `--background-color` | 背景色，必须使用 solid hex | `#F5F4ED` |
| `--max-width` | 内容最大宽度（px） | `640` |
| `--output` | 输出文件路径 | 自动生成 |
| `--components` | 启用组件拓展层（6 个结构化组件） | `false`（默认纯净模式） |

## 输出规则

**默认输出路径：**
- 输入：`path/to/article.md`
- 输出：`path/to/article_wechat.html`

**输出内容：**
1. 完整的 HTML 文件
2. 内联样式（可直接复制到公众号）
3. 保留图片链接
4. 自动处理代码块、引用块、列表等

## 工作流程

1. **读取 Markdown 文件**
   - 解析 frontmatter（标题、摘要等）
   - 提取正文内容

2. **加载主题配置**
   - 读取主题参数
   - 应用用户自定义参数

3. **转换为 HTML**
   - Markdown → HTML 结构
   - 应用主题样式（内联）
   - 处理特殊元素（代码、图片、引用）

4. **输出文件**
   - 生成完整 HTML
   - 保存到指定路径
   - 输出使用说明

## 主题预览

不确定选哪个主题？使用主题预览生成器对比所有主题效果：

```bash
# 生成所有主题的预览页面（使用默认示例文章）
node scripts/generate-preview.mjs

# 使用自定义文章生成预览
node scripts/generate-preview.mjs path/to/your-article.md

# 只预览指定主题（逗号分隔，无空格）
node scripts/generate-preview.mjs article.md --themes magazine-ink,magazine-indigo,magazine-forest

# 自定义输出路径
node scripts/generate-preview.mjs article.md --themes kami,elegant --output /path/to/my-preview.html
```

预览页面会并排展示所选主题的效果，方便快速对比选择。生成的 `preview.html` 可以在浏览器中打开查看。

## 扩展新主题

**步骤：**

1. 在 `themes/` 目录创建新主题配置文件：
   ```yaml
   # themes/my-theme.yaml
   name: my-theme
   description: 我的自定义主题
   font_family_cn: 'Custom Font CN'
   font_family_en: 'Custom Font EN'
   font_size: 16
   line_height: 1.8
   accent_color: '#ff6b6b'
   background_color: '#f8f9fa'
   heading_font: 'Heading Font'
   code_font: 'Code Font'
   ```

2. 使用新主题：
   ```bash
   /wechat-styler article.md --theme my-theme
   ```

## 公众号兼容硬规则

以下规则由 `scripts/validate.mjs` **确定性执行**，不依赖模型自觉。convert 产物自动校验；独立运行 `node scripts/validate.mjs output.html` 可复检（0 ERROR 退出 0，有 ERROR 退出 1，给 CI/自动化用）。

convert 采用**软门**策略：发现 ERROR 时文件照常生成（用户能先看效果），末尾打印红色报告明细；独立 validate 脚本才返回非零退出码。

### ERROR 级（产物必须为 0，否则粘贴后会出问题）

1. **禁用标签**：`<style>` / `<script>` / `<link>` / `<iframe>` / body 内 `<meta>` / `<input>`
   - 原因：公众号编辑器剥离，导致样式/脚本/外部资源失效
2. **禁用属性**：`class=` / `id=` / `contenteditable`
   - 原因：公众号编辑器剥离，样式必须全部内联到 `style`
3. **禁用 CSS**：`position:fixed|absolute` / `display:grid|flex` / `@media` / `@keyframes`
   - 原因：粘贴后错位、布局坍塌或被忽略
4. **禁用函数**：`rgba()` / `hsla()`
   - 原因：背景色在编辑器中丢失，必须用 solid hex（如 `#1B365D`，非 `rgba(27,54,93,0.8)`）
5. **禁用外部字体**：`@font-face` 的 `url(...)` 外部引用
   - 原因：加载失败降级，版式走样；用系统字体栈

### WARN 级（建议修复，不阻断）

6. **图片无 alt**：`<img>` 缺 `alt` 属性（无障碍 + 图床失效时的兜底）
7. **图片偏移风险**：`<img>` 缺 `margin:0 auto` 或 `display:block`（粘贴后可能偏左）
8. **块级元素缺 style**：`<p>` / `<h2>` / `<blockquote>` 缺 `style` 属性（粘贴后样式丢失）

### convert.mjs 已内置的兼容策略（无需手动处理）

- 所有背景色使用 solid hex，不用 `rgba()`
- 外层 section / 内容 section / 文本 span 三层重复声明 `background-color`，降低粘贴后背景丢失
- 图片父级 `text-align:center` + 自身 `margin:0 auto;display:block` 双重兜底，防止偏移
- 所有样式内联，不使用 `<style>` 标签或外部 CSS

## 占位符机制

写作时图床还没准备好，但想先看排版效果？在 Markdown 里写占位符，convert 会渲染成居中虚线灰框：

```markdown
这是一段正文。

【插入:文章开头的视频截图】

继续正文。
```

渲染效果：克制中性灰虚线框 + 居中灰字「📷 待补素材：xxx」，不抢正文视觉。图准备好后，把 `【插入:xxx】` 替换成 `![alt](url)` 即可。

只支持独占一行的 `【插入:xxx】`（全角方括号）；行内不会触发，避免误伤正文。

## 组件拓展层（可选）

需要结构化呈现「对比关系」「操作流程」「关键金句」「提示旁注」时，加 `--components` 参数启用 6 个结构化组件。**默认不启用**——90% 的场景用纯净排版就够，组件拓展层是按需付费的可选能力。

### 两种模式

```bash
# 默认模式（纯净）：组件语法会被优雅降级成普通 markdown 元素，不暴露
node scripts/convert.mjs article.md --theme zhijian

# 组件模式：6 个组件语法被识别并升级成结构化 HTML
node scripts/convert.mjs article.md --theme zhijian --components
```

默认模式下，所有组件语法（`:::flow`、`> [!NOTE]`、`1. [step]` 等）会 fallback 成普通有序列表、无序列表或引用块，不会出现乱码或暴露标记。用户不需要学任何组件语法，skill 行为跟纯 markdown 转换器一模一样。

### 6 个组件

| 组件 | 语法 | 视觉形态 | 适用场景 |
|------|------|----------|----------|
| 金句块 | `> **核心观点**` | 居中 + 楷体大字 + 上下留白 | 文章核心论点、关键金句 |
| 提示块 | `> [!NOTE] 内容` | 结构色（墨蓝）前缀 + 同行正文 | 补充说明、技术旁注 |
| 警告块 | `> [!WARNING] 内容` | 强调色（暖陶）前缀 + 同行正文 | 注意事项、踩坑提醒 |
| 步骤序号 | `1. [step] 动作` | 加粗数字 01/02/03 + 正文 | 操作流程、动作清单 |
| 流程卡片 | `:::flow` 围栏 | section + flex 横排 + 箭头 | 输入→处理→输出、阶段流程 |
| 对比卡片 | `:::compare` 围栏 | section + flex 多栏 | 方案 A vs B vs C |
| 时间线 | `:::timeline` 围栏 | 竖向圆点 + 竖线 | 演进历程、项目复盘 |

### 组件语法示例

```markdown
## 金句块

> **员工效率不等于组织效能。**

## 提示与警告

> [!NOTE] 沉淀成 Skill 而不是文档，Skill 自带执行力。

> [!WARNING] 这三步的顺序不能颠倒。

## 步骤序号

1. [step] 先对齐 90 天能看见结果的小目标。
2. [step] 选一个高频高价值的场景切入。
3. [step] 把跑通的过程沉淀成 Skill。

## 流程卡片

:::flow
对齐目标 → 选场景试点 → 沉淀成 Skill
:::

## 对比卡片（**包裹** 表示高亮项）

:::compare
**克制派 · 推荐** | wechat-styler | 沉淀在 Skill
组件派 | gzh-design | 沉淀在组件库
手工派 | 秀米 | 沉淀在 PPT
:::

## 时间线

:::timeline
2026 · 03 | v1.0 初版 | 3 套基础主题
2026 · 07 | v1.5 组件拓展层 | 6 个结构化组件
:::
```

### 设计原则

- **克制优于装饰**：组件不用色块，只靠排印手段（字号、字体、留白、细线）+ section/flex 布局建立层次
- **颜色从主题取**：所有组件的颜色/字体从当前主题的 yaml 配置取，各主题自动适配，不写死任何颜色
- **不用 table**：公众号编辑器对 `<table>` 会强制灰边框，组件全部用 `section + display:flex`（实测兼容）
- **默认沉默**：不传 `--components` 时，组件语法优雅降级成普通 markdown，不增加任何认知负担

## 示例

**输入 Markdown：**
```markdown
---
title: 文章标题
summary: 文章摘要
---

## 章节标题

这是一段正文，包含**加粗**和`代码`。

![图片说明](https://example.com/image.png)

> 这是一段引用
```

**输出 HTML：**
- 完整的公众号可用 HTML
- 所有样式内联
- 可直接复制粘贴

## 技术实现

**核心脚本：** `scripts/convert.mjs`（转换）+ `scripts/validate.mjs`（公众号兼容性校验）+ `scripts/components.mjs`（组件拓展层，可选）

**依赖：**
- Node.js 18+
- marked（Markdown 解析）
- js-yaml（YAML 解析）

**目录结构：**
```
wechat-styler/
├── SKILL.md
├── scripts/
│   ├── convert.mjs          # Markdown → 公众号 HTML（软门调用 validate）
│   ├── validate.mjs         # 公众号兼容性校验（独立可运行 / 被 convert 引用）
│   ├── components.mjs       # 组件拓展层（6 个结构化组件，--components 启用）
│   └── generate-preview.mjs # 主题预览页生成器
├── themes/
│   ├── elegant.yaml
│   ├── kami.yaml
│   ├── magazine-forest.yaml
│   ├── magazine-indigo.yaml
│   ├── magazine-ink.yaml
│   ├── modern.yaml
│   ├── minimal.yaml
│   └── zhijian.yaml
└── templates/
    └── base.html
```

---

**最后更新：** 2026-07-07
**版本：** 1.5.0
**作者：** 大鹏
