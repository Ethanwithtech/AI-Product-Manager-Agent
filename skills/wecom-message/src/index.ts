/**
 * WeCom MCP Server
 * 
 * Send messages to WeCom (企业微信) via incoming webhooks
 * 
 * Usage:
 *   npm install
 *   npm run build
 *   export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
 *   node dist/index.js
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import axios from "axios";
import FormData from "form-data";
import fs from "fs";
import path from "path";

const WECOM_WEBHOOK_URL = process.env.WECOM_WEBHOOK_URL;
const WECOM_TIMEOUT_MS = parseInt(process.env.WECOM_TIMEOUT_MS || "10000", 10);

if (!WECOM_WEBHOOK_URL) {
  console.error("Error: WECOM_WEBHOOK_URL environment variable is required");
  process.exit(1);
}

/** Get webhook key from WECOM_WEBHOOK_URL for upload_media API */
function getWebhookKey(): string {
  const url = WECOM_WEBHOOK_URL;
  if (!url) throw new Error("WECOM_WEBHOOK_URL is required");
  const key = new URL(url).searchParams.get("key");
  if (!key) {
    throw new Error("WECOM_WEBHOOK_URL must contain a key parameter");
  }
  return key;
}

/** Upload file to WeCom and return media_id (valid for 3 days) */
async function uploadMedia(filePath: string, type: "file" | "voice" = "file"): Promise<string> {
  const key = getWebhookKey();
  const uploadUrl = `https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=${key}&type=${type}`;
  const stat = fs.statSync(filePath);
  if (stat.size <= 5) {
    throw new Error("File size must be greater than 5 bytes");
  }
  if (type === "file" && stat.size > 20 * 1024 * 1024) {
    throw new Error("File size must not exceed 20MB for type=file");
  }
  if (type === "voice" && stat.size > 2 * 1024 * 1024) {
    throw new Error("Voice file size must not exceed 2MB");
  }
  const form = new FormData();
  form.append("media", fs.createReadStream(filePath), {
    filename: path.basename(filePath),
    knownLength: stat.size,
  });
  const response = await axios.post(uploadUrl, form, {
    timeout: WECOM_TIMEOUT_MS,
    headers: form.getHeaders(),
    maxContentLength: Infinity,
    maxBodyLength: Infinity,
  });
  if (response.data?.errcode !== 0 && response.data?.errcode !== undefined) {
    throw new Error(`WeCom upload error: ${response.data.errmsg}`);
  }
  return response.data.media_id;
}

const server = new Server({
  name: "wecom-message",
  version: "1.0.3",
});

// Register server capabilities
server.registerCapabilities({
  tools: {},
});

// Tool: send_wecom_message
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "send_wecom_message") {
    const content = args?.content as string;
    const mentioned_list = args?.mentioned_list as string[] | undefined;

    if (!content) {
      throw new Error("content is required");
    }

    try {
      const response = await axios.post(
        WECOM_WEBHOOK_URL,
        {
          msgtype: "text",
          text: {
            content,
            mentioned_list: mentioned_list || [],
          },
        },
        {
          timeout: WECOM_TIMEOUT_MS,
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.data?.errcode !== 0 && response.data?.errcode !== undefined) {
        throw new Error(`WeCom API error: ${response.data.errmsg}`);
      }

      return {
        content: [
          {
            type: "text",
            text: "Message sent to WeCom successfully",
          },
        ],
      };
    } catch (error: any) {
      throw new Error(`Failed to send WeCom message: ${error.message}`);
    }
  }

  if (name === "send_wecom_markdown") {
    const content = args?.content as string;

    if (!content) {
      throw new Error("content is required");
    }

    try {
      const response = await axios.post(
        WECOM_WEBHOOK_URL,
        {
          msgtype: "markdown",
          markdown: {
            content,
          },
        },
        {
          timeout: WECOM_TIMEOUT_MS,
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.data?.errcode !== 0 && response.data?.errcode !== undefined) {
        throw new Error(`WeCom API error: ${response.data.errmsg}`);
      }

      return {
        content: [
          {
            type: "text",
            text: "Markdown message sent to WeCom successfully",
          },
        ],
      };
    } catch (error: any) {
      throw new Error(`Failed to send WeCom markdown: ${error.message}`);
    }
  }

  if (name === "upload_wecom_media") {
    const file_path = args?.file_path as string;
    const type = (args?.type as "file" | "voice") || "file";
    if (!file_path) {
      throw new Error("file_path is required");
    }
    if (!fs.existsSync(file_path) || !fs.statSync(file_path).isFile()) {
      throw new Error(`File not found or not a file: ${file_path}`);
    }
    try {
      const media_id = await uploadMedia(file_path, type);
      return {
        content: [
          {
            type: "text",
            text: `Uploaded successfully. media_id: ${media_id} (valid for 3 days)`,
          },
        ],
      };
    } catch (error: any) {
      throw new Error(`Failed to upload WeCom media: ${error.message}`);
    }
  }

  if (name === "send_wecom_file") {
    let media_id = args?.media_id as string | undefined;
    const file_path = args?.file_path as string | undefined;
    if (file_path) {
      if (!fs.existsSync(file_path) || !fs.statSync(file_path).isFile()) {
        throw new Error(`File not found or not a file: ${file_path}`);
      }
      try {
        media_id = await uploadMedia(file_path, "file");
      } catch (error: any) {
        throw new Error(`Failed to upload file before send: ${error.message}`);
      }
    }
    if (!media_id) {
      throw new Error("Either media_id or file_path is required");
    }
    try {
      const response = await axios.post(
        WECOM_WEBHOOK_URL,
        {
          msgtype: "file",
          file: { media_id },
        },
        {
          timeout: WECOM_TIMEOUT_MS,
          headers: { "Content-Type": "application/json" },
        }
      );
      if (response.data?.errcode !== 0 && response.data?.errcode !== undefined) {
        throw new Error(`WeCom API error: ${response.data.errmsg}`);
      }
      return {
        content: [
          {
            type: "text",
            text: "File message sent to WeCom successfully",
          },
        ],
      };
    } catch (error: any) {
      throw new Error(`Failed to send WeCom file: ${error.message}`);
    }
  }

  throw new Error(`Unknown tool: ${name}`);
});

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "send_wecom_message",
        description: "Send a text message to WeCom via webhook",
        inputSchema: {
          type: "object",
          properties: {
            content: {
              type: "string",
              description: "Message content to send",
            },
            mentioned_list: {
              type: "array",
              description: "List of userids to mention (WeCom userids)",
              items: {
                type: "string",
              },
            },
          },
          required: ["content"],
        },
      },
      {
        name: "send_wecom_markdown",
        description: "Send a markdown message to WeCom via webhook",
        inputSchema: {
          type: "object",
          properties: {
            content: {
              type: "string",
              description: "Markdown content to send",
            },
          },
          required: ["content"],
        },
      },
      {
        name: "upload_wecom_media",
        description: "Upload a file or voice to WeCom and get media_id (valid 3 days). Use for sending file/voice messages later.",
        inputSchema: {
          type: "object",
          properties: {
            file_path: {
              type: "string",
              description: "Absolute or relative path to the file to upload",
            },
            type: {
              type: "string",
              enum: ["file", "voice"],
              description: "Media type: file (≤20MB) or voice (≤2MB, AMR only)",
            },
          },
          required: ["file_path"],
        },
      },
      {
        name: "send_wecom_file",
        description: "Send a file message to WeCom. Provide media_id from upload_wecom_media, or file_path to upload and send in one step.",
        inputSchema: {
          type: "object",
          properties: {
            media_id: {
              type: "string",
              description: "media_id from upload_wecom_media (valid 3 days)",
            },
            file_path: {
              type: "string",
              description: "Path to file: uploads then sends (alternative to media_id)",
            },
          },
        },
      },
    ],
  };
});

// Start server
const transport = new StdioServerTransport();
server.connect(transport);

console.error("wecom-message MCP Server running on stdio");
