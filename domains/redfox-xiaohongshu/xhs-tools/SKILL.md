---
id: redfox-xiaohongshu/xhs-tools
domain: redfox-xiaohongshu
name: xhs-tools
description: 小红书运营工具集。两个子命令：(1) /xhs-cover 生成 1080×1440 竖屏封面（从 wallpapercave 拉高清图 + 顶部小标 + 底部大标 + 描边阴影）；(2) /xhs-video 用蝉镜数字人 API 把文案自动转成口播视频（支持列出可用数字人 + 选择人物 + 调语速）。触发词："小红书封面"、"xhs 封面"、"1080x1440"、"数字人"、"蝉镜"、"口播视频"、"xhs 视频"、"chanjing"。用来批量生产小红书爆款视觉素材（封面 CTR 10%+）/ 视频内容（均赞 25x 优于图文）。
version: 1.0.0
origin: redfox-data/redfox-community
license: MIT
---


# XHS Tools · 小红书运营工具集

两个独立命令，单文件 SKILL.md。在 `scripts/` 里有两个 Python 脚本（`xhs_cover.py`、`chanjing_video.py`）。

## 触发 → 命令路由

| 用户说 | 调命令 |
|--------|--------|
| "做个小红书封面"、"xhs 封面"、"1080×1440 封面"、"我的标题是 X，封面排个版" | **`/xhs-cover`** |
| "做个蝉镜视频"、"数字人口播"、"把这段文案转视频"、"chanjing 生成" | **`/xhs-video`** |
| 同时需要封面 + 视频 | 先 `/xhs-cover`，再 `/xhs-video` |

两个命令**不互相依赖** —— 跑哪个都行。

---

## /xhs-cover — 小红书封面生成

### Resolve `SKILL_DIR`（任何命令都先做这一步）

读 `~/.claude/skills/xhs-tools/SKILL.md`（或 Claude Code plugin cache、agents cache 路径），该路径就是 `SKILL_DIR`。脚本在 `${SKILL_DIR}/scripts/xhs_cover.py`。

**Windows 提醒**：`Scripts/**/*.py` 用 `E:\Python\python.exe`（不能直接用 `python3`，Windows 的 `python3` 是 Microsoft Store stub）。其它平台用 `python3`。

```bash
SKILL_DIR="C:\Users\maning\.claude\skills\xhs-tools"
if [ ! -f "$SKILL_DIR/scripts/xhs_cover.py" ]; then
  echo "ERROR: scripts/xhs_cover.py not found under $SKILL_DIR" >&2
  exit 1
fi
```

### 输入参数

| 参数 | 必填 | 说明 | 默认 |
|------|------|------|------|
| `--title` / `-t` | ✅ | 顶部小标（54px） | — |
| `--subtitle` / `-s` | ✅ | 底部大标（90px） | — |
| `--color` / `-c` | — | 文字颜色（不带 `#`） | `C8102E`（葡萄牙/意大利红） |
| `--wp-id` | — | wallpapercave 壁纸 ID（如 `wp14175359`） | `wp14175359` |
| `--output` / `-o` | — | 输出路径 | `~/Desktop/cover_<wp>.png` |
| `--test <id1> <id2> …` | — | 批量测试壁纸 ID 可用性，不生成封面 | — |

### 工作流

```
Step 1  拿用户输入：title + subtitle（颜色可选，用主题色：体育/赛事=C8102E，科技=1F4E79，美食=E07B0E）
Step 2  不熟悉壁纸 ID → 先 --test 几个常见 ID（wp14175359 / wp16088006 / wp13623633）
Step 3  确认 wallpapercave 可用 → 跑：
            python "$SKILL_DIR/scripts/xhs_cover.py" \
              --title "C罗不在场" --subtitle "葡萄牙反而赢了" --color C8102E
Step 4  输出在桌面，agent 自动 Read 把 PNG 显示给用户
```

### 颜色速查

| 内容主题 | 推荐色（去掉 #） |
|---------|-------------------|
| 体育 / 赛事 / 争议 | `C8102E` 红 |
| 科技 / 数码 / AI | `1F4E79` 深蓝 |
| 自然 / 美食 / 生活方式 | `2E7D32` 绿 |
| 娱乐 / 明星 / 八卦 | `6A1B9A` 紫 |
| 时事 / 政治 | `B71C1C` 暗红 |

### 实战配方

```bash
# 足球热点
python "$SKILL_DIR/scripts/xhs_cover.py" \
  --title "C罗不在场" --subtitle "葡萄牙反而赢了" --color C8102E

# 批量测试可用壁纸
python "$SKILL_DIR/scripts/xhs_cover.py" \
  --test wp14175359 wp16088006 wp13623633 wp17286051 wp17824299
```

---

## /xhs-video — 蝉镜数字人口播视频

### Resolve `SKILL_DIR`（同样规则）

`SKILL_DIR=<读到的 SKILL.md 所在目录>`

脚本在 `${SKILL_DIR}/scripts/chanjing_video.py`。

### 前置：API 凭证

读取顺序（自动优先级）：
1. 命令行参数：`--app-id <id> --secret-key <key>`
2. 环境变量：`CHANJING_APP_ID` + `CHANJING_SECRET_KEY`
3. 配置文件：`~/.chanjing/config.json`（`{"app_id":"...","secret_key":"..."}`）

**首次使用**：用 `AskUserQuestion` 问用户"有蝉镜 API 吗"。如有 → 写文件 + 设为 chmod 600；如无 → 引导去 https://open-api.chanjing.cc 申请。

### 输入参数

| 参数 | 必填 | 说明 | 默认 |
|------|------|------|------|
| `text` 或 `--text` | ✅ | 口播文案（≤2000 字） | — |
| `--person` / `-p` | — | 数字人 ID（先用 `--list` 看可用） | `ce393722...`（海城） |
| `--figure` | — | 全身 / 坐姿 / 圆形视角 | `whole_body` |
| `--speed` / `-s` | — | 语速 0.5–2.0 | 1.0 |
| `--output` / `-o` | — | 输出 mp4 路径 | `chanjing_output.mp4` |

### 工作流

```
Step 1  --list 列出数字人 → 选一个
Step 2  没有配置文件 → 写 ~/.chanjing/config.json（chmod 600）
Step 3  跑：python "$SKILL_DIR/scripts/chanjing_video.py" "你的文案"
Step 4  提交后会返回 video_id，agent 持续轮询直到 status=30（成功），下载 mp4
Step 5  agent 把 mp4 路径给用户，必要时推荐"下一步：推到小红书后台"用 MCP
```

### 实战配方

```bash
# 列数字人
python "$SKILL_DIR/scripts/chanjing_video.py" --list

# 标准用法
python "$SKILL_DIR/scripts/chanjing_video.py" \
  "世界杯4年1次，熬夜看球是成年人最后的浪漫"

# 调语速 + 换数字人
python "$SKILL_DIR/scripts/chanjing_video.py" \
  --text "你的长文案，控制在 2000 字内" \
  --person <新 ID> --speed 1.2 \
  --output "F:\\自媒体\\videos\\post.mp4"
```

### 预估时长

字数 × 234 / 1000 ≈ 秒（基于系统 TTS 1.0 语速）

### 失败模式

| 错误 | 处理 |
|------|------|
| Token 获取失败 / `code != 0` | 检查 AppID/SecretKey，再问用户确认 |
| status >= 40 | 报错 + 删除任务，让用户重新发起 |
| 5 分钟还没好 | timeout，提示用户稍后 `--list` 或重试 |

---

## 触发 → 输出 总结（agent 怎么回应用户）

成功 `/xhs-cover` → "封面已生成到 `~/Desktop/cover_xxx.png`（1800x2400 jpg），用 `Read` 工具预览，CTR 高的封面 = 1) 人物 / 产品实体 2) 强反差色块 3) 不超过 12 个字标题"

成功 `/xhs-video` → "蝉镜视频已下到 `output.mp4`（时长 X 秒，数字人：海城），需要我帮你检查 / 加封面 / 直接发小红书吗？"

---

## 文件结构

```
xhs-tools/
├── SKILL.md                ← 本文
├── README.md               ← 项目文档
└── scripts/
    ├── xhs_cover.py        ← 封面生成（1080×1440）
    └── chanjing_video.py    ← 蝉镜视频 API 调用
```

依赖：`pip install Pillow requests`（skimage/imagemagick 都不需要）

---

## 安全 / 副作用

- xhs_cover.py：从 wallpapercave 拉图（公开），写一张 PNG 到桌面，**自动删除** 中间临时文件
- chanjing_video.py：调用 `open-api.chanjing.cc`（国内域，无 GFW 问题），生成 mp4 写盘
- 两个脚本都不读敏感配置文件（蝉镜 config.json 自己管理）
