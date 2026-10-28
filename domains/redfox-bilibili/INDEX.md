# redfox-bilibili — 红狐·B站

> **触发场景**：B站搜索、UP主作品、评论、关键词账号、B站榜单
> **技能数**：7　|　**来源**：redfox-data/redfox-community

| 技能 | 中文标签 | 关键词（中文 / 英文） | 路径 | 大小 |
|---|---|---|---|---|
| `B站关键词搜作品` | B站关键词搜作品 | B站搜索,B站最新视频,B站热门,B站搜作品,bilibili搜索,要求搜索B站最新内容,查看某关键词下的视频数据,搜索B站最新内容 / b站关键词搜作品工具。根据用户输入的关键词调用 redfox 接口搜索b站最新视频，支持按排序方式和发布时间筛选，返回新鲜数据（非缓存/历史… | `domains/redfox-bilibili/B站关键词搜作品/SKILL.md` | 8.7K |
| `bili-ai-feed` | B站AI信息源 — 每日扫描B站AI相关 | B站爆款,AI-B站热点,B站AI内容,B站AI视频,重要,禁止自动调用接口,API Key 获取,配置方式 / "b站ai信息源 — 每日扫描b站ai相关账号，按点赞量发现爆款视频，智能聚类话题后生成包含封面图、互动数据与订阅支持的html日报。同时基… | `domains/redfox-bilibili/bili-ai-feed/SKILL.md` | 12.3K |
| `bilibili-comment` | B站评论分析 | B站评论,B站视频评论,评论查询,评论分析,评论舆情,看评论,bilibili评论,需要查看B站视频评论,分析评论舆情 / b站评论分析工具。输入b站视频链接或bv号即可获取一级评论数据，支持分页浏览、评论情感分析（积极/负面/需求/竞品），生成精美 html 报… | `domains/redfox-bilibili/bilibili-comment/SKILL.md` | 5.8K |
| `bilibili-keywords-accounts` | B站关键词搜账号 | 需要搜索B站账号,查找B站UP主,找B站同类账号,等级,简介等信息 | `domains/redfox-bilibili/bilibili-keywords-accounts/SKILL.md` | 2.2K |
| `bilibili-portfolio-search` | B站账号作品列表实时查询 | B站账号视频,UP主投稿列表 / b站账号作品列表实时查询工具。根据b站up主的uid获取该up主发布的最新视频作品列表，支持游标翻页浏览更多作品。当用户想查看某个b站up主… | `domains/redfox-bilibili/bilibili-portfolio-search/SKILL.md` | 1.8K |
| `cultural-tourism-bilibili-feed` | 文旅B站信息源 — 搜索文旅相关B站热门 | 文旅B站,文旅信息源,文旅资讯,旅游B站,景区视频,文旅爆款,需要文旅B站,旅游攻略,景区热度 / 文旅b站信息源 — 搜索文旅相关b站热门视频，按点赞量筛选最火内容，生成精美 html 报告。当用户需要文旅b站、旅游攻略、景区热度、文旅资… | `domains/redfox-bilibili/cultural-tourism-bilibili-feed/SKILL.md` | 4.5K |
| `playlet-bili-feed` | B站短剧爆款内容追踪 | 分析短剧题材趋势,重要,禁止自动调用接口,⚡ 智能日期判断,🎨 B站风格日报,📊 零值隐藏,🔄 批量查询,配置方式 / b站短剧爆款内容追踪工具，每日自动扫描b站短剧创作内容，按点赞量筛选爆款作品，智能聚类题材后生成可视化html日报与创作趋势分析。当用户需要… | `domains/redfox-bilibili/playlet-bili-feed/SKILL.md` | 14.0K |

> 读法：拿用户需求里的关键词去对「关键词」列，命中哪一行就拉哪个路径的 SKILL.md。

> 红狐社媒采集系列。**务必靠「关键词」列定位单个技能**，不要整域拉取。部分技能需要红狐 API 凭证。
