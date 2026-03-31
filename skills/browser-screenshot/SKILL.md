---
name: browser-screenshot
description: >-
  浏览器自动化与截图。支持三种引擎：本地 Playwright 脚本、ClawHub playwright-mcp（MCP 服务器）、
  ClawHub browser-use（智能浏览器代理）。可截取全页/元素/移动端，也可自动浏览、表单填充、数据提取。
  当需要截取网页、竞品页面、产品 UI 截图用于 PRD，或需要自动化浏览器交互收集信息时使用。
  触发词：截图、screenshot、网页截图、竞品截图、浏览器自动化、browser-use、playwright。
type: component
theme: pm-tools
best_for:
  - "截取竞品网页做对比分析"
  - "截取自家产品页面放入 PRD 做 UI 设计参考"
  - "自动化浏览竞品网站收集定价、功能列表等信息"
  - "模拟移动端截图验证响应式设计"
  - "PRD 中涉及 UI 功能设计时，自动附加产品截图"
scenarios:
  - "帮我截一下竞品官网首页，我要放在 PRD 里做对比"
  - "截取我们产品的 dashboard 页面，全页截图"
  - "用 iPhone 视角截一下这个页面看看移动端效果"
  - "自动浏览竞品定价页，提取所有套餐信息"
  - "PRD 里涉及了搜索功能改造，帮我截取现在的搜索界面作为 Before 图"
---

# Browser Screenshot — 浏览器截图工具

## Purpose

产品经理在写 PRD、做竞品分析、准备评审材料时，经常需要截取网页。手动截图费时且不标准化（不同人截的尺寸、范围都不同）。这个 Skill 通过 Playwright 自动化浏览器，提供标准化、可重复的截图能力。

它支持三种截图模式：
- **全页截图**：从顶到底完整截取（适合长页面）
- **可视区域截图**：只截取浏览器窗口可见部分
- **元素截图**：通过 CSS 选择器精准截取页面中的某个区域

_为什么用 Playwright 而不是简单的 HTTP 请求？因为现代网页大量使用 JavaScript 动态渲染，需要真实浏览器环境才能正确截图。Playwright 的 Chromium 引擎保证了和用户看到的一致。_

## Prerequisites

本 Skill 支持三种引擎，按需选择：

### 引擎 A：本地 Playwright 脚本（轻量，仅截图）

```bash
pip3 install playwright
python3 -m playwright install chromium
```

### 引擎 B：ClawHub playwright-mcp（MCP 服务器，支持完整浏览器自动化）

来自 ClawHub，作者 shawnpana（2.8 万下载量）。通过 MCP 协议提供浏览器自动化能力。

```bash
# 安装 SkillHub CLI
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/install.sh | bash

# 安装 playwright-mcp skill
skillhub install playwright-mcp
```

安装后在 `.mcp.json` 中会自动添加 playwright-mcp 服务器配置。Agent 可通过 MCP 协议调用浏览器导航、点击、表单填充、截图、数据提取等能力。

### 引擎 C：ClawHub browser-use（智能浏览器代理，最强大）

来自 ClawHub，作者 spiceman161（2.4 万下载量）。提供 AI 驱动的智能浏览器代理，可理解页面语义并自主操作。

```bash
skillhub install browser-use
```

**三种引擎对比**：

| 能力 | 本地脚本 | playwright-mcp | browser-use |
|------|---------|---------------|-------------|
| 全页/元素/设备截图 | ✅ | ✅ | ✅ |
| 导航和点击 | ❌ | ✅ | ✅ |
| 表单填充 | ❌ | ✅ | ✅ |
| 数据提取 | ❌ | ✅ | ✅ |
| 语义理解页面内容 | ❌ | ❌ | ✅ |
| 多步骤自动化工作流 | ❌ | ✅ | ✅ |
| 需要 MCP | ❌ | ✅ | ✅ |
| 安装复杂度 | 低 | 中 | 中 |

**推荐**：
- 只需截图 → 引擎 A（本地脚本）
- 需要自动化浏览 + 截图 → 引擎 B（playwright-mcp）
- 需要智能交互（如自动登录、多步采集）→ 引擎 C（browser-use）

## PRD 自动截图规则

当 PM Strategist Agent 在 Synthesizer 阶段生成 PRD 时，**如果方案涉及 UI 功能设计变更**，自动触发截图流程：

### 触发条件

以下任一条件满足即触发：
- 方案中提到"界面改造"、"UI 变更"、"交互优化"、"页面重设计"
- 方案中涉及具体页面或功能模块（如"搜索页"、"dashboard"、"设置页"）
- 用户明确要求"截图"、"要有界面参考"

### 自动执行流程

```
1. 识别方案中涉及的 UI 页面 URL（从 Researcher 的代码分析中获取）
2. 对每个页面调用截图（桌面 + 移动端各一张）
3. 将截图嵌入 PRD 的对应章节：
   - "Solution Design" 部分 → 添加"当前界面（Before）"截图
   - 如有竞品参考 → 添加竞品截图
4. 截图文件保存在 ./screenshots/ 目录
5. PRD 中用 Markdown 图片语法引用：![当前搜索页](./screenshots/search_page.png)
```

### PRD 截图格式规范

```markdown
### UI 参考（自动截取）

#### 当前界面 (Before)
| 桌面端 | 移动端 |
|--------|--------|
| ![桌面端](./screenshots/desktop_current.png) | ![移动端](./screenshots/mobile_current.png) |

#### 竞品参考（如有）
| 竞品 A | 竞品 B |
|--------|--------|
| ![竞品A](./screenshots/competitor_a.png) | ![竞品B](./screenshots/competitor_b.png) |

> 以上截图由 browser-screenshot Skill 自动截取，截取时间：YYYY-MM-DD HH:MM
```

## Key Concepts

### 三种截图模式

| 模式 | 参数 | 适用场景 |
|------|------|---------|
| **全页截图** | 默认 | 长落地页、文档页、需要看全貌 |
| **可视区域** | `--viewport-only` | 首屏分析、折叠以上内容 |
| **元素截图** | `--selector ".class"` | 只要页面中某个组件（如定价表、导航栏） |

### 设备模拟

支持 Playwright 内置的所有设备预设（iPhone、iPad、Pixel 等），用于验证响应式设计或截取移动端视角。

### Cookie 注入

对需要登录才能访问的页面（如内部系统、SaaS 后台），可以通过 `--cookies` 参数注入 Cookie 文件。Cookie 格式与 `wecom-doc-skills-v2` 的 `export_cookies.py` 输出兼容。

## Application

### 基础用法

```bash
# 全页截图（默认）
python3 <skill_dir>/scripts/screenshot.py https://example.com

# 输出到指定路径
python3 <skill_dir>/scripts/screenshot.py https://example.com -o ./competitor-homepage.png

# 只截可视区域
python3 <skill_dir>/scripts/screenshot.py https://example.com --viewport-only

# 截取特定元素
python3 <skill_dir>/scripts/screenshot.py https://example.com --selector ".pricing-section"
```

> `<skill_dir>` 为本 SKILL.md 所在目录，使用时替换为绝对路径。

### 高级用法

```bash
# 自定义视口大小（宽屏显示器）
python3 <skill_dir>/scripts/screenshot.py https://example.com --width 1920 --height 1080

# 模拟 iPhone 13
python3 <skill_dir>/scripts/screenshot.py https://example.com --device "iPhone 13"

# 等待某个元素加载后再截图（适合动态内容）
python3 <skill_dir>/scripts/screenshot.py https://example.com --wait-for ".data-loaded"

# 额外等待 3 秒（等动画结束）
python3 <skill_dir>/scripts/screenshot.py https://example.com --delay 3

# 需要登录的页面（注入 Cookie）
python3 <skill_dir>/scripts/screenshot.py https://internal-dashboard.com --cookies ~/.wecom-cookies.json
```

### 在 PM Strategist 中的使用场景

PM Strategist Agent 可在以下阶段调用此 Skill：

| 阶段 | 场景 | 示例 |
|------|------|------|
| **Researcher** | 截取竞品页面做视觉分析 | 截取竞品的定价页、功能页、首页 |
| **Synthesizer** | 为方案附加可视化参考 | 截取现有产品界面作为"改造前"参考 |
| **Validator** | 验证方案涉及的页面是否真如描述 | 确认某个功能确实存在于当前产品中 |

### 批量截图

在脚本中循环调用即可实现批量截图：

```python
import subprocess

urls = [
    "https://competitor-a.com",
    "https://competitor-b.com",
    "https://competitor-c.com",
]

for url in urls:
    subprocess.run([
        "python3", "<skill_dir>/scripts/screenshot.py",
        url, "-o", f"./screenshots/{url.split('//')[1].replace('/', '_')}.png"
    ])
```

## Parameters Reference

| 参数 | 缩写 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | — | (必填) | 目标网页 URL |
| `--output` | `-o` | 自动生成 | 输出文件路径 |
| `--viewport-only` | — | False | 仅截取可视区域 |
| `--selector` | `-s` | None | CSS 选择器（截取特定元素） |
| `--width` | — | 1280 | 视口宽度 |
| `--height` | — | 720 | 视口高度 |
| `--wait-for` | — | None | 等待指定选择器出现 |
| `--wait-timeout` | — | 30000 | 等待超时（毫秒） |
| `--device` | — | None | 模拟设备名称 |
| `--delay` | — | 0 | 额外等待秒数 |
| `--cookies` | — | None | Cookie JSON 文件路径 |

## Examples

### 示例 1：竞品首页对比截图

**场景**：PM 需要在 PRD 中对比三个竞品的首页设计。

```bash
python3 <skill_dir>/scripts/screenshot.py https://slack.com -o ./screenshots/slack.png --width 1440
python3 <skill_dir>/scripts/screenshot.py https://discord.com -o ./screenshots/discord.png --width 1440
python3 <skill_dir>/scripts/screenshot.py https://teams.microsoft.com -o ./screenshots/teams.png --width 1440
```

### 示例 2：移动端截图验证

**场景**：验证产品在 iPhone 上的显示效果。

```bash
python3 <skill_dir>/scripts/screenshot.py https://your-product.com --device "iPhone 13" -o ./mobile-check.png
```

### 示例 3：只截取定价区域

**场景**：竞品分析只关心定价表。

```bash
python3 <skill_dir>/scripts/screenshot.py https://competitor.com/pricing --selector ".pricing-table" -o ./competitor-pricing.png
```

## Common Pitfalls

### 反模式 1：截取动态内容不等待

**症状**：截图中图表是空的、数据没加载出来。

**原因**：页面使用异步 JavaScript 加载数据，截图在数据到达前就执行了。

**修复**：使用 `--wait-for` 等待数据容器出现，或用 `--delay` 等几秒。

### 反模式 2：不注入 Cookie 截登录后页面

**症状**：截图结果是登录页面，不是目标页面。

**修复**：先用 `wecom-doc-skills-v2` 的 `export_cookies.py` 导出 Cookie，再通过 `--cookies` 注入。

### 反模式 3：全页截图截了几万像素高的页面

**症状**：无限滚动页面截出超大图片（10MB+），打开卡死。

**修复**：对无限滚动页面使用 `--viewport-only` 只截首屏，或 `--selector` 截取特定区域。

## References

### Related Skills
- `skills/wecom-doc-skills-v2/SKILL.md` — 使用相同的 Playwright + Chromium 基础设施，可复用其 Cookie 导出机制
- `skills/tapd-toolkit/SKILL.md` — 截图后可通过 TAPD toolkit 上传到 TAPD 需求单
- `skills/pm-strategist/SKILL.md` — PM Strategist 在 Researcher 阶段可调用此 Skill 截取竞品界面

### Related Agents
- `agents/pm-strategist.md` — 产品策划 Agent 可在竞品研究和方案佐证时调用截图

### Dependencies
- Python 3.9+
- Playwright (`pip3 install playwright`)
- Chromium (`python3 -m playwright install chromium`)

---

_Skill type: component_
_Suggested filename: SKILL.md_
_Suggested placement: skills/browser-screenshot/_
_Dependencies: Playwright + Chromium installed_
