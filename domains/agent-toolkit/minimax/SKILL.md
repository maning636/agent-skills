---
id: agent-toolkit/minimax
domain: agent-toolkit
name: minimax
description: Use MiniMax CLI (mmx) for image generation, video generation, speech synthesis, music generation, and image understanding. Activate when the user asks to generate/create images, videos, audio, or music, or when they ask about their quota.
origin: 本机自研
license: 见来源
---


# MiniMax CLI (mmx)

Multi-modal AI generation tools via the `mmx` CLI. Requires prior authentication with `mmx auth login --api-key <key>`.

## Prerequisites

If `mmx` is not found, install it:

```bash
npm install -g mmx-cli
```

For Chinese users experiencing 401 errors, set the region:

```bash
mmx config set --key region --value cn
```

---

## Tools

### Image Generation

```bash
mmx image generate --prompt "描述内容"
```

Outputs a generation task ID, then polls until the image is ready. Returns the file path on completion.

**When to use**: User says "画一张...", "生成图片", "create an image of...", etc.

---

### Video Generation

```bash
mmx video generate --prompt "描述内容"
```

Starts a video generation task. Use `mmx video task get <task-id>` to check status. Video generation typically takes 1-3 minutes.

**When to use**: User says "做个视频", "生成视频", "create a video of...", etc.

---

### Speech Synthesis

```bash
mmx speech synthesize --text "要转换的文字"
```

Converts text to speech. Returns the audio file path.

**When to use**: User says "配音", "读出来", "文字转语音", "text to speech", etc.

---

### Music Generation

```bash
mmx music generate --prompt "描述音乐风格和内容"
```

Generates music based on the description. Check quota with `mmx quota` first — music generation has limited quota.

**When to use**: User says "生成音乐", "创作音乐", "create music...", etc.

---

### Image Understanding / Vision

```bash
mmx vision describe <图片路径>
```

Analyzes an image and returns a description. Accepts local file paths or URLs.

**When to use**: User shares an image and asks "这是什么", "描述这张图", "what's in this image", etc.

---

### Text Chat

```bash
mmx text chat --message "对话内容"
```

Simple text conversation with MiniMax models.

**When to use**: Direct MiniMax text对话 when not using the main agent.

---

### Check Quota

```bash
mmx quota
```

Shows current Token Plan usage and quota limits. Useful to check remaining credits before generation tasks.

**When to use**: User asks "还有多少额度", "查看配额", "check quota", "remaining credits", etc.

---

## Quick Reference

| Task | Command |
|------|---------|
| 生成图片 | `mmx image generate --prompt "..."` |
| 生成视频 | `mmx video generate --prompt "..."` |
| 语音合成 | `mmx speech synthesize --text "..."` |
| 音乐生成 | `mmx music generate --prompt "..."` |
| 图片理解 | `mmx vision describe <path>` |
| 文本对话 | `mmx text chat --message "..."` |
| 查看配额 | `mmx quota` |
| 查看配置 | `mmx config show` |
| 认证状态 | `mmx auth status` |

---

## Notes

- Image generation: check `mmx quota` for image-01 quota limits
- Video generation: async task — may need to poll for completion
- Music generation: quota is limited (music-2.6 and music-cover models)
- Chinese users should set `region: cn` if 401 errors occur