# 小红书运营工具集 (XHS Tools)

## 工具

| 脚本 | 功能 | 用法 |
|------|------|------|
| `scripts/chanjing_video.py` | 蝉镜数字人口播视频生成 | `python chanjing_video.py "你的文案"` |
| `scripts/xhs_cover.py` | 小红书封面生成 (1080×1440) | `python xhs_cover.py --title "标题" --subtitle "副标题"` |

## 前置

```bash
pip install requests Pillow
```

## 蝉镜视频生成

```bash
# 列出可用数字人
python scripts/chanjing_video.py --list

# 生成视频
python scripts/chanjing_video.py "世界杯4年1次，熬夜看球是成年人最后的浪漫"
```

凭证自动读取 `~/.chanjing/config.json`。

## 封面生成

```bash
# 用指定壁纸ID生成封面
python scripts/xhs_cover.py --wp-id wp14175359 --title "C罗不在场" --subtitle "葡萄牙反而赢了" --color C8102E

# 批量测试壁纸ID
python scripts/xhs_cover.py --test wp14175359 wp16088006 wp13623633
```

## 数据复盘 (6/10-6/16)

**结论**: 日产5篇AI图文 = 点赞崩溃 (6.0→0.2)。视频内容25倍优于图文。蝉镜数字人 + C罗争议帖 = 止跌方案。

| 指标 | AI图文 (旧) | 视频+争议图文 (新) |
|------|------------|-------------------|
| 日发帖 | 5篇图文 | 1视频 + 1图文 |
| 封面CTR | 2.3% | 10%+ (球星真图) |
| 均赞 | 0.2 | 25+ (视频) |
| 蝉镜接入 | ❌ | ✅ chanjing_video.py |
