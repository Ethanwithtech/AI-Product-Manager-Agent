---
name: skill-navigator
description: >-
  当用户不确定该用哪个 Skill、问"有什么功能"、"能做什么"、"帮我找个合适的工具"时使用此技能。
  也在 AI 不确定该调用哪个 Skill 时作为路由索引使用。列出当前所有可用的 64 个 Skill
  并按场景分类，帮助快速定位最合适的 Skill。
type: component
theme: meta
best_for:
  - "用户问有哪些功能或能力"
  - "用户不确定该用哪个 Skill"
  - "AI 需要在多个 Skill 中选择最合适的一个"
  - "新用户首次使用想了解全貌"
---

# Skill Navigator — 技能导航索引

## Purpose

这是一个**路由索引 Skill**。当用户不确定该用哪个 Skill、或者 AI 面对模糊需求时，先查阅本索引找到最匹配的 Skill，再调用对应 Skill 执行。

**使用规则：**
1. 用户问"有什么功能" / "能做什么" / "帮我找工具" → 展示分类索引
2. 用户需求模糊，多个 Skill 都可能匹配 → 查本索引，推荐最合适的 1-3 个并解释区别
3. 找到目标 Skill 后，**直接切换到该 Skill 执行**，不要停在本索引

---

## 全部 Skill 索引（64 个）

### 🔍 发现与研究（11 个）

| Skill | 干什么 | 什么时候用 |
|-------|--------|-----------|
| `company-research` | 公司/竞品深度调研 | 要了解某个公司的产品、战略、组织架构 |
| `customer-journey-map` | 画客户旅程地图 | 需要梳理用户从接触到付费的完整体验 |
| `customer-journey-mapping-workshop` | 带团队做旅程地图工作坊 | 多人协作完成旅程梳理 |
| `discovery-interview-prep` | 准备用户访谈 | 要去访谈用户前的准备工作 |
| `discovery-process` | 跑完整 Discovery 流程 | 从问题假设到方案验证的完整周期 |
| `jobs-to-be-done` | JTBD 分析 | 想搞清楚用户真正想完成什么任务 |
| `lean-ux-canvas` | Lean UX 画布 | 梳理假设、实验和学习目标 |
| `opportunity-solution-tree` | 机会解决方案树 | 从目标出发系统找机会和方案 |
| `problem-framing-canvas` | 问题框架画布 | 觉得问题没定义清楚 |
| `problem-statement` | 写问题陈述 | 需要一句话说清楚问题是什么 |
| `proto-persona` | 快速用户画像 | 还没做正式研究但需要先画个用户画像 |

### 🎯 战略与规划（10 个）

| Skill | 干什么 | 什么时候用 |
|-------|--------|-----------|
| `pestel-analysis` | 宏观环境分析 | 进入新市场、评估外部环境影响 |
| `positioning-statement` | 产品定位语句 | 需要说清楚"我们是谁、给谁用、有什么不同" |
| `positioning-workshop` | 定位工作坊 | 团队一起讨论定位 |
| `prd-development` | 系统化写 PRD | 需要完整的产品需求文档 |
| `press-release` | Amazon 式新闻稿 | 用 Working Backwards 方法倒推产品价值 |
| `prioritization-advisor` | 选优先级框架 | 一堆需求不知道怎么排序 |
| `product-strategy-session` | 产品战略会话 | 需要做战略对齐 |
| `roadmap-planning` | 路线图规划 | 规划季度或年度路线图 |
| `tam-sam-som-calculator` | 市场规模估算 | 需要知道市场有多大 |
| `eol-message` | 产品下线公告 | 要关停某个功能或产品 |

### 📦 交付与拆解（7 个）

| Skill | 干什么 | 什么时候用 |
|-------|--------|-----------|
| `epic-breakdown-advisor` | 拆 Epic 为用户故事 | Epic 太大需要拆 |
| `epic-hypothesis` | 把需求变假设 | 想让需求变成可验证的 |
| `storyboard` | 六格故事板 | 需要可视化用户场景 |
| `user-story` | 写用户故事 | 需要标准格式的用户故事 |
| `user-story-mapping` | 故事地图 | 按用户流程组织所有故事 |
| `user-story-mapping-workshop` | 故事地图工作坊 | 带团队一起做故事地图 |
| `user-story-splitting` | 拆分大故事 | 一个故事太大没法估点 |

### 💰 商业与财务（7 个）

| Skill | 干什么 | 什么时候用 |
|-------|--------|-----------|
| `acquisition-channel-advisor` | 获客渠道评估 | 判断某个渠道值不值得投 |
| `business-health-diagnostic` | SaaS 业务诊断 | 想知道业务整体健康状况 |
| `feature-investment-advisor` | 功能投资决策 | 判断某个功能值不值得做 |
| `finance-based-pricing-advisor` | 定价变更分析 | 准备调价想预判影响 |
| `finance-metrics-quickref` | 财务指标速查 | 快速查某个指标的定义和算法 |
| `saas-economics-efficiency-metrics` | 单位经济模型 | 分析 CAC、LTV、回收期等 |
| `saas-revenue-growth-metrics` | 收入增长指标 | 算 MRR、流失率、NRR 等 |

### 🚀 职业发展（4 个）

| Skill | 干什么 | 什么时候用 |
|-------|--------|-----------|
| `altitude-horizon-framework` | PM→Director 心智模型 | 想理解管理层思维和 IC 的区别 |
| `director-readiness-advisor` | PM→Director 过渡 | 准备 Director 面试或刚上任 |
| `executive-onboarding-playbook` | VP/CPO 上任 90 天 | 新上任高管的诊断式上手计划 |
| `vp-cpo-readiness-advisor` | Director→VP/CPO | 想往更高管理层发展 |

### 🤖 AI 产品能力（5 个）

| Skill | 干什么 | 什么时候用 |
|-------|--------|-----------|
| `ai-shaped-readiness-advisor` | AI 就绪度评估 | 评估团队 AI 成熟度 |
| `context-engineering-advisor` | 上下文工程诊断 | 给 AI 很多资料结果还是差 |
| `pol-probe` | 低成本验证实验 | 设计最小验证实验 |
| `pol-probe-advisor` | 选验证方式 | 该用什么类型的原型验证 |
| `recommendation-canvas` | AI 产品评估画布 | 评估 AI 功能的可行性和价值 |

### 🛠 元能力与工具（2 个）

| Skill | 干什么 | 什么时候用 |
|-------|--------|-----------|
| `workshop-facilitation` | 工作坊引导协议 | 被其他 Interactive Skill 自动引用 |
| `skill-authoring-workflow` | 创建新 Skill | 想把自己的方法论变成 Skill |

### 👥 PM 团队工具包（6 个）

| Skill | 干什么 | 什么时候用 |
|-------|--------|-----------|
| `product-knowledge-base` | 知识库管理 | 搭建或维护团队产品知识库 |
| `requirement-generator` | 快速生成 PRD | 从一句话需求快速生成结构化文档 |
| `ui-draft-generator` | 生成 UI 初稿 | 根据需求直接出 React 代码 |
| `product-sync-agent` | 团队进度同步 | 检查团队工作冲突和负载 |
| `fullchain-efficiency` | 需求到 UI 一条龙 | 知识检索→PRD→UI 全自动 |
| `feedback-insight-engine` | 反馈分析与讨论 | 分析标书、评价、工单、访谈等反馈 |

### 🔧 效率工具（6 个）

| Skill | 干什么 | 什么时候用 |
|-------|--------|-----------|
| `browser-screenshot` | 浏览器网页截图 | 截取竞品页面、产品界面、移动端截图，支持全页/元素/设备模拟 |
| `docx` | Word 文档操作 | 创建、编辑、读取 .docx 文件 |
| `pdf` | PDF 文件操作 | 读取、合并、拆分、加水印 PDF |
| `multi-perspective-evaluation` | 多角度评估 | 从 5 个维度（怀疑者/用户拥护者/执行者/远见者/系统思考者）评估方案 |
| `tapd-toolkit` | TAPD 扩展工具 | 上传图片/附件到 TAPD、查询下载附件 |
| `woa-preview` | 内网文档预览 | 把文档发布到 pages.woa.com 在线查看 |

### 📱 通讯与协作（3 个）

| Skill | 干什么 | 什么时候用 |
|-------|--------|-----------|
| `tencent-meeting-mcp` | 腾讯会议管理 | 预约/修改/取消会议、查录制、查转写和 AI 纪要 |
| `wecom-message` | 企微消息发送 | 通过 Webhook 发消息到企业微信群 |
| `wecom-doc-skills-v2` | 企微文档操作 | 读取和操作企业微信云文档 |

### 🎵 AI 能力扩展（2 个）

| Skill | 干什么 | 什么时候用 |
|-------|--------|-----------|
| `asr-sentence-recognition` | 语音识别 | 把音频转成文字（短/长/超长音频） |
| `xiaohongshu-mcp` | 小红书运营 | 发布内容、搜索笔记、分析评论 |

---

## 快速决策树

遇到用户需求时，按这个顺序判断：

```
用户想做什么？
│
├─ 写文档/PRD/报告 ──→ requirement-generator / prd-development / docx
├─ 产品策划/方案规划 ──→ pm-strategist（自主五角色推演 + GAN 对抗循环）
├─ 分析反馈/数据 ──→ feedback-insight-engine / business-health-diagnostic
├─ 排优先级/决策 ──→ prioritization-advisor / feature-investment-advisor / multi-perspective-evaluation
├─ 了解用户/市场 ──→ discovery-process / jobs-to-be-done / tam-sam-som-calculator
├─ 团队协作/同步 ──→ product-sync-agent / tencent-meeting-mcp / wecom-message
├─ 操作文件 ──→ pdf / docx / tapd-toolkit
├─ 发布/预览 ──→ woa-preview / xiaohongshu-mcp
├─ 语音/音频 ──→ asr-sentence-recognition
├─ 不确定/想看全貌 ──→ 展示本索引的分类表
└─ 职业发展 ──→ altitude-horizon-framework / director-readiness-advisor
```

## Common Pitfalls

### ❌ 停在导航不执行
**错误**：用户说"帮我写 PRD"，AI 回复"你可以用 requirement-generator"然后等着。
**正确**：找到匹配 Skill 后直接切换过去执行，不要让用户再说一遍。

### ❌ 推荐太多 Skill
**错误**：列出 5 个可能相关的 Skill 让用户自己选。
**正确**：推荐最匹配的 1 个，如果确实有歧义，最多给 2-3 个并说清区别。

### ❌ 忽略新增的效率工具
**错误**：用户说"帮我操作 PDF"但 AI 不知道有 pdf Skill。
**正确**：效率工具类（docx/pdf/tapd-toolkit 等）也是正式 Skill，同样应该被索引和调用。
