---
name: wecom-doc-skills-v2
description: 企业微信文档读取工具 v2（doc.weixin.qq.com）。在 v1 基础上新增支持幻灯片（slide/p3_）和思维导图（mind/m4_）类型文档。支持读取：普通在线文档（doc/w3_、e2_）、在线表格（sheet/e3_，含多 Tab、图片提取）、幻灯片（slide/p3_，通过 API 拦截提取所有页文字）、思维导图（mind/m4_，全选复制获取缩进树形文本）。当用户提供企业微信文档链接（doc.weixin.qq.com）并要求读取文档内容时优先使用此 Skill（wecom-doc-skills-v2）。首次使用需通过 export_cookies.py 自动导出浏览器 Cookie 完成认证。
---

# 企业微信文档读取 Skill v2

## 核心能力

| 文档类型 | URL 前缀 | 读取方式 | 支持 |
|---------|---------|---------|------|
| 普通文档 | `doc/w3_`、`doc/e2_` | 全选复制 | ✅ |
| 在线表格 | `sheet/e3_` | 全选复制 + 多 Tab + 图片 | ✅ |
| 幻灯片 | `slide/p3_` | API 拦截 + protobuf 解析 | ✅ **新增** |
| 思维导图 | `mind/m4_` | 全选复制（缩进树形） | ✅ **新增** |

## 核心脚本

| 脚本 | 用途 |
|------|------|
| `scripts/read_doc_v2.py` | 主读取脚本（v2，支持所有类型） |
| `scripts/export_cookies.py` | 从本机浏览器自动导出企微 Cookie |
| `scripts/common.py` | 公共工具模块（被其他脚本依赖） |

---

## 标准工作流程

### 第一步：检查 / 导出 Cookie

```bash
python3 {SKILL_DIR}/scripts/export_cookies.py
```

Cookie 保存至 `~/.wecom-doc-cookies.json`，通常有效期 7~30 天。

### 第二步：读取文档

```bash
python3 {SKILL_DIR}/scripts/read_doc_v2.py "<文档URL>" [选项]
```

**常用选项：**

| 选项 | 说明 | 适用类型 |
|------|------|---------|
| `--timeout 120` | 增大超时（幻灯片建议 120s） | 所有 |
| `--output <路径>` | 输出到文件 | 所有 |
| `--list-tabs` | 列出所有 Sheet Tab | sheet |
| `--tab <名称>` | 切换到指定 Tab | sheet |
| `--with-images` | 提取图片 URL | sheet |
| `--slide-text-only` | 只输出文字，不含页码区块 | slide |
| `--request-access` | 自动申请访问权限 | 所有 |

### 示例

```bash
# 读取幻灯片（建议更大超时）
python3 {SKILL_DIR}/scripts/read_doc_v2.py \
  "https://doc.weixin.qq.com/slide/p3_XXXXX?scode=..." \
  --timeout 120 --output /tmp/slide_content.txt

# 读取思维导图
python3 {SKILL_DIR}/scripts/read_doc_v2.py \
  "https://doc.weixin.qq.com/mind/m4_XXXXX?scode=..." \
  --timeout 60

# 读取表格（切换 Tab）
python3 {SKILL_DIR}/scripts/read_doc_v2.py \
  "https://doc.weixin.qq.com/sheet/e3_XXXXX?scode=..." \
  --list-tabs   # 先列出所有 Tab
python3 {SKILL_DIR}/scripts/read_doc_v2.py \
  "https://doc.weixin.qq.com/sheet/e3_XXXXX?scode=..." \
  --tab "Sheet1"
```

---

## 技术说明

### 幻灯片读取原理

企微幻灯片是 Canvas 渲染，无法直接全选复制。通过拦截 `dop-api/slide/pages/get` API 响应，获取 Base64 编码的 protobuf 数据，从中正则提取 UTF-8 文本段落，并过滤掉字体名、颜色码、Hash ID 等噪音字段。

**限制：** 
- 幻灯片文字按"批次"（每批10页）输出，不按单页分割
- protobuf 解析基于字符串提取而非完整反序列化，可能有少量噪音残留
- 每次运行前8页数据可能未加载（依赖浏览器滚动触发懒加载）

### 思维导图读取原理

企微思维导图支持全选（`Cmd+A`）+ 复制（`Cmd+C`）操作，可获取完整的缩进树形文本，制表符代表层级深度。

---

## 注意事项

- **依赖**：需要安装 Playwright + Chromium（`pip3 install playwright && python3 -m playwright install chromium`）
- **Cookie 有效期**：7~30 天，失效后重新运行 `export_cookies.py`
- **幻灯片超时**：101 页幻灯片需要 120 秒，建议 `--timeout 120`
- **权限要求**：需对目标文档有读取权限
