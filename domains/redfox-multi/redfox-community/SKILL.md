---
id: redfox-multi/redfox-community
domain: redfox-multi
name: redfox-community
description: RedFoxHub 技能合集入口：88 个子技能已按平台拆分到 redfox-xiaohongshu / redfox-douyin / redfox-bilibili / redfox-wechat / redfox-multi 五个域，本文件只作合集说明与上游索引。
origin: redfox-data/redfox-community
license: 见来源
---

# RedFox Community

RedFoxHub 技能合集。共 88 个可复用 sub-skill，覆盖灵感、选题、文案创作、数据复盘等场景。

## 子技能在哪里

本库把 88 个子技能**按平台拆进 5 个域**，每个子技能都是标准 L2 目录（自带 `references/`、`assets/`、`scripts/`）：

| 域 | 覆盖平台 | 目录 |
|---|---|---|
| `redfox-xiaohongshu` | 小红书 | `domains/redfox-xiaohongshu/` |
| `redfox-douyin` | 抖音 | `domains/redfox-douyin/` |
| `redfox-bilibili` | B站 | `domains/redfox-bilibili/` |
| `redfox-wechat` | 公众号 | `domains/redfox-wechat/` |
| `redfox-multi` | 通用 / 聚合 / AI搜索 / 股票 / 视频 | `domains/redfox-multi/` |

## 怎么用

1. 读对应域的 `INDEX.md`，用「关键词」列定位**单个**技能——不要整域拉取。
2. 只取那个技能的 `SKILL.md`，附属文件按它的指引再取。
3. 部分技能需要红狐 API 凭证。

上游仓库：<https://github.com/redfox-data/redfox-community>（原始 88 个子技能仍以 `skills/<name>/` 平铺存放）。
本目录下的 `README.md` / `README.en.md` 为上游原始说明。
