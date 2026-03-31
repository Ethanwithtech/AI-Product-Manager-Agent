---
name: wecom-message
description: "Send messages to WeCom (企业微信) via webhooks using MCP protocol. Works with Claude Code, Claude Desktop, and other MCP clients."
---

# WeCom Skill (v1.0.3)

Send text, markdown, and **file** messages to `WeCom` (`企业微信`) via incoming webhooks (ENV: `WECOM_WEBHOOK_URL`).

`WeCom` is the enterprise version (using in office) of the famous all-in-on IM `WeChat` envied by Elon Musk.

## Setup

```bash
# Navigate to skill directory
cd skills/wecom-message

# Install dependencies
npm install

# Build TypeScript
npm run build

# Set webhook URL
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
```

## Usage with Claude Code

Add to your `~/.config/claude_code/mcp.json`:

```json
{
  "mcpServers": {
    "wecom-message": {
      "command": "node",
      "args": ["/path/to/clawdbot/skills/wecom-message/dist/index.js"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
      }
    }
  }
}
```

Then restart Claude Code. You'll have tools for text, markdown, and file messages.

# Tools

## `send_wecom_message`

Send a text message to WeCom.

```bash
# Simple message
await send_wecom_message({ content: "Hello from OpenClaw!" });

# With mentions
await send_wecom_message({
  content: "Meeting starting now",
  mentioned_list: ["zhangsan", "lisi"]
});
```

## `send_wecom_markdown`

Send a markdown message (WeCom flavor).

```bash
await send_wecom_markdown({
  content: `# Daily Report
  
**Completed:**
- Task A
- Task B

**Pending:**
- Task C

<@zhangsan>`
});
```

## `upload_wecom_media`

Upload a file or voice to WeCom and get `media_id` (valid for **3 days**). Use this when you want to send the same file later, or to get a `media_id` for voice messages.

```bash
# Upload a file (for later send_wecom_file)
await upload_wecom_media({ file_path: "/path/to/report.pdf" });

# Upload as voice (type=voice: ≤2MB, AMR only, ≤60s)
await upload_wecom_media({ file_path: "/path/to/audio.amr", type: "voice" });
```

| Limit | Value |
|-------|--------|
| All files | > 5 bytes |
| Ordinary file (`type=file`) | ≤ 20 MB |
| Voice (`type=voice`) | ≤ 2 MB, AMR only, play length ≤ 60s |
| `media_id` validity | 3 days |

## `send_wecom_file`

Send a file message to the group. Either pass a `media_id` from `upload_wecom_media`, or a `file_path` to upload and send in one step.

```bash
# Send by media_id (after upload_wecom_media)
await send_wecom_file({ media_id: "1G6nrLmr5EC3MMb_-zK1dDdzmd0p7cNliYu9V5w7o8K0" });

# Upload and send in one step
await send_wecom_file({ file_path: "/path/to/report.pdf" });
```

**Note:** `media_id` is only valid for the same webhook (robot); do not reuse across different bots.

# WeCom Markdown Tags

WeCom supports:

| Feature | Syntax |
|---------|--------|
| Bold | `**text**` or `<strong>text</strong>` |
| Italic | `*text*` or `<i>text</i>` |
| Strikethrough | `~~text~~` or `<s>text</s>` |
| Mention | `<@userid>` |
| Link | `<a href="url">text</a>` |
| Image | `<img src="url" />` |
| Font size | `<font size="5">text</font>` |
| Color | `<font color="#FF0000">text</font>` |

# Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WECOM_WEBHOOK_URL` | Yes | - | WeCom webhook URL |
| `WECOM_TIMEOUT_MS` | No | 10000 | Request timeout (ms) |

# How To

Get `WECOM_WEBHOOK_URL` following steps here, and envolve it as a bot into a group chat:

(Tip: You should get the `WECOM_WEBHOOK_URL` entirely as a URL, NOT just a KEY )

### STEP 1

![STEP 1](https://cdn.jsdelivr.net/gh/qidu/qidu.github.io@main/public/images/wecom/step1_wecom.png)

### STEP 2

![STEP 2](https://cdn.jsdelivr.net/gh/qidu/qidu.github.io@main/public/images/wecom/step2_wecom.png)

### STEP 3

![STEP 3](https://cdn.jsdelivr.net/gh/qidu/qidu.github.io@main/public/images/wecom/step3_wecom.png)

### STEP 4

![STEP 4](https://cdn.jsdelivr.net/gh/qidu/qidu.github.io@main/public/images/wecom/step4_wecom.png)

# Reference

[消息推送配置说明（含文件/语音上传接口）](https://developer.work.weixin.qq.com/document/path/99110)

[Download WeCom Apps](https://work.weixin.qq.com/#indexDownload)
