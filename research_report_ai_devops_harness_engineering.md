# AI DevOps 与 Harness Engineering 深度研究报告

## 执行摘要

本报告深入研究两个在 2025-2026 年 AI 工程领域最受关注的概念：AI DevOps 和 Harness Engineering。AI DevOps 是将人工智能深度融入软件开发和运维全流程的新范式，标志着从"自动化时代"向"智能体时代"的跃迁。Harness Engineering（驾驭工程）则是 2026 年初横空出世的 AI Agent 工程方法论，核心公式为 Agent = Model + Harness，主张通过构建模型之外的约束、反馈和控制系统来实现 AI Agent 的可靠运行。两者在理念上高度相通——都强调"系统级的控制与约束"而非单纯依赖模型能力。然而，Harness Engineering 是否是 AI Agent 的"最佳标准"，业界存在深刻的路线之争，Latent Space 将其概括为 Big Model vs Big Harness 的对立。本报告将逐一拆解这些概念，呈现不同派别的理解差异，并给出综合判断。

---

## 第一部分：AI DevOps——从自动化到智能体化

### 什么是 AI DevOps

传统 DevOps 是 Development 和 Operations 的组合词，由 Patrick Debois 于 2009 年首次提出，核心是打破开发与运维之间的壁垒，通过自动化流程实现持续集成、持续交付（CI/CD）。AI DevOps 则是在此基础上，将大语言模型（LLM）、异常检测算法、根因分析引擎等 AI 技术深度融合到 DevOps 全流程中，实现从"规则驱动的自动化"向"数据驱动的智能决策"的范式转变。

具体而言，AI DevOps 覆盖了软件生命周期的每一个环节。在开发阶段，AI 可以自动生成代码、进行智能代码审查。GitHub Copilot、GitLab Duo 等工具已经成为许多团队的标配，研究表明 AI 辅助的代码审查可以将软件交付性能提升约 50%。在 CI/CD 管道中，AI 不再是边缘辅助角色，而是进入了关键路径——它可以根据代码变更的语义自动决定运行哪些测试子集、分析构建失败的根因、甚至生成修复补丁。在运维侧，AIOps（Artificial Intelligence for IT Operations）通过七层架构实现了从数据采集到自动化执行的完整闭环，核心功能包括异常检测、根因分析、预测预警和自愈修复。

### IDC FutureScape 2026：关键门槛

IDC 中国研究经理王彦翔指出，开发者和 DevOps 正站在从"自动化时代"迈向"智能体时代"的关键门槛。过去 20 年 DevOps 的核心问题是"人如何写代码、交付系统"，而随着 Agentic AI 的成熟，问题变成了"如何治理、管理和监督智能体"。IDC 预测，到 2030 年 80% 的开发者将与自主 AI 智能体协作，65% 的企业将把 AI 智能体深度嵌入 DevOps/DevSecOps 流水线。但同时也警告，70% 的"自建型"智能体 AI 项目将因未达成 ROI 而被放弃，主要原因是低估了治理、运维和组织成本。

这意味着 AI DevOps 的成功不仅仅取决于技术，更取决于企业是否具备平台工程能力、AI 治理机制和开发者角色转型规划。换言之，AI DevOps 的核心挑战已经从"怎么用 AI"转变为"怎么管 AI"——这恰恰是 Harness Engineering 试图回答的问题。

---

## 第二部分：Harness Engineering——概念起源与核心定义

### 概念的诞生

Harness Engineering 的诞生可以追溯到一条清晰的时间线。2025 年底，HashiCorp 联合创始人、Terraform 作者 Mitchell Hashimoto 在博客中率先提出核心思想："每当 Agent 犯错，就花时间工程化一个机制，确保它永远不再犯同样错误。"2026 年 2 月 5 日，他在技术分享中正式公开命名 Harness Engineering。仅六天后的 2 月 11 日，OpenAI 发布了轰动性的百万行代码实验报告——一个 3 人团队用 Codex Agent 在 5 个月内构建了供数百人使用的 Beta 产品，生成近 100 万行代码，全程零人工编写。随后，Martin Fowler（ThoughtWorks 首席科学家）撰文深度分析，Anthropic 发布了长时运行 Agent 的 Harness 设计框架。一个月内，Harness Engineering 从一个个人博客上的新词，迅速成为整个 AI 工程社区最热门的话题。

### 核心定义

Harness Engineering 的核心公式极其简洁：**Agent = Model + Harness**。

Model 是大语言模型本身，负责推理和生成；Harness 是模型之外的一切——包括系统提示词、工具调用、文件系统、沙箱环境、编排逻辑、钩子中间件、反馈回路和约束机制。一个形象的比喻是：模型是 CPU，Harness 是操作系统。CPU 再强，如果操作系统拉胯，整体体验也会崩盘。

更准确地说，Harness Engineering 是围绕 AI Agent 设计和构建约束机制、反馈回路、工作流控制和持续改进循环的系统工程实践。它不优化模型本身，而是优化模型运行的"环境"。核心哲学八个字：**人类掌舵，智能体执行**。

### 三代范式的演进

理解 Harness Engineering 需要将其放在 AI 工程方法论演进的脉络中。

第一代是 Prompt Engineering（2022-2024），关注单次交互质量，核心假设是"写对指令即可解决问题"，工程师的工作是调优 Prompt 措辞。它类似于写一封措辞完美的邮件。但当 AI 开始承担多步骤任务时，单次指令优化无法解决记忆、状态和推理连续性问题。

第二代是 Context Engineering（2024-2025），关注知识与记忆管理，核心问题是"模型看什么"。它通过 RAG、对话历史管理、知识库检索等手段提升模型的信息环境质量。这相当于给员工准备完整的工作简报。但信息环境再好，也无法保证执行的稳定性和失败恢复。

第三代便是 Harness Engineering（2026 至今），关注整个运行环境，核心问题是"系统怎么让 Agent 稳定把长链路任务做完"。这相当于设计整个公司的制度和流程。三者是嵌套关系：Prompt 包含于 Context，Context 包含于 Harness。

---

## 第三部分：为什么说这是一个"哈姆雷特式"问题

### 不同派别的理解差异

你的观察非常精准——Harness Engineering 确实是一个"一千个人眼中有一千个哈姆雷特"的问题。不同的组织和个人基于各自的实践经验和利益立场，对同一概念发展出了截然不同的理解框架。

**Anthropic——流程控制派。** Anthropic 的理解侧重于通过严格流程确保 Agent 按步骤执行。他们提出了三智能体架构：Planner（规划者）负责将用户需求扩展为完整规格，Generator（执行者）负责写代码，Evaluator（评估者）用 Playwright 像真实用户一样测试应用。关键机制包括 JSON 物理锁（任务清单由初始化 Agent 生成，执行 Agent 只能改状态不能篡改描述，防止虚标完成）、Context Reset（上下文满了就彻底清空启动全新 Agent，仅通过结构化文件交接）、以及 Sprint Contract（冲刺合同，开工前双方协商验收标准）。实验数据显示，单 Agent 基线耗时 1 小时 9 分、成本 3.53 美元但核心功能坏掉；三 Agent 框架耗时 3 小时 38 分、成本 79.20 美元但功能完整可靠。虽然成本高 20 倍，但质量实现了质的飞跃。

**OpenAI——环境控制派。** OpenAI 的理解侧重于仓库准确性和环境设计。他们的核心信条是"仓库即现实"——Agent 只能理解仓库内的内容，外部文档等于不存在。具体实践包括：AGENTS.md 采用渐进式披露策略，从百科全书转变为约 100 行的导航目录，指向深层文档；架构约束通过自定义 Linter 和 CI 门禁机械强制执行，Agent 违反规则就无法合入代码；88 个 AGENTS.md 文件覆盖不同子系统，每一行规则都源自过去的一次具体失败；还有专门的"文档园丁 Agent"负责清理过时文档，防止错误记忆。在这套体系下，人类不再直接编写代码，而是专注于系统设计、环境配置和反馈循环。

**Cursor 团队——架构与并发派。** Cursor 的理解侧重于大规模 Agent 并发的调度和协作。他们建立了 Planner-Worker-Judge 三层架构，使用 DAG（有向无环图）进行单行道调度，确定性节点与概率性节点交替运行。从 Team Mode 的实现来看，Agent 从"一次性临时工"进化为"长期驻留的队友"，支持点对点通信。Cursor 团队的一个关键发现是优先级排序：Prompt > Harness > 模型。在架构成熟后，调整 Prompt 对系统行为的影响最大，其次是 Harness 架构调整，最后才是更换模型本身。

**Martin Fowler——理论框架派。** Fowler 提供了系统论的理论框架，将 Harness 组件分为两类：前馈引导器（Governors）在生成之前引导 Agent 行为，包括架构文档、编码规范、ESLint 配置等；反馈传感器（Sensors）在生成之后帮助 Agent 自我纠错，包括单元测试、类型检查、AI 代码审查等。他基于 Ashby 定律提出"约束即自由"的原则——通过限制解题空间反而提升可靠性。

### Big Model vs Big Harness 路线之争

这场争论在 Latent Space 于 2026 年 3 月发布的标志性文章《Is Harness Engineering Real?》中达到高潮，将整个行业分成了两大阵营。

**Big Model 阵营**认为秘密全在模型里，Harness 应该是最薄的封装。代表人物包括 Claude Code 团队的 Boris Cherny 和 Cat Wu，他们强调代码极其简单，刻意保持"最极简的版本"；以及 OpenAI 的 Noam Brown，他认为以前为弥补非推理模型不足而建立的复杂 Agent 系统，在推理模型出现后变得不再必要甚至有害。METR 和 Scale AI 的评估数据也显示，Claude Code 这样的复杂 Harness 相比基础 Scaffold 在某些场景下并没有明显统计优势，选择哪种 Harness 可能只是误差范围内的噪声。

**Big Harness 阵营**认为 Harness 就是产品本身，是释放 AI 价值的关键。代表人物 Jerry Liu（LangChain）认为"Model Harness is Everything"。最有力的证据来自一项实验：仅仅改变 Harness 而不改模型，LangChain 在 TerminalBench 2.0 上的成功率从 52.8% 提升到 66.5%；Can.ac 只改变了编辑接口格式，成功率从 6.7% 跳到 68.3%。这证明 Harness 具有独立于模型的商业和技术价值。

### 争议的深层原因

这场争论之所以如此激烈，根本原因在于它不仅是技术问题，更是哲学和商业利益的冲突。如果"秘密在模型"，那么 Harness 工程就是短期应急方案，模型公司是最终赢家。如果"秘密在系统"，那么 Harness 工程就是长期竞争优势，应用层公司有独立价值。

最具洞察力的观点来自对 Claude Code 泄漏源码的分析，提出了"补偿面迁移"概念。核心观点是：Harness 的每一个组件都是一块补丁，贴在模型当前做不到的缺陷上。随着模型能力提升（如从 Opus 4.5 到 4.6），某些补丁变得不再必要，必须果断拆除。Anthropic 在升级模型后主动移除了 Context Reset 机制就是一个实例。这意味着护城河不在 Harness 的厚度，而在追踪补偿面迁移的速度——知道何时该加、何时该拆。

---

## 第四部分：Harness Engineering 与 AI DevOps 的深层关联

### 理念的相通

你的老师提到"如何设计 AI DevOps 的机制跟 Harness Engineering 的理念很像"，这个观察是完全准确的。两者在核心理念上高度相通，都在回答同一个问题：**当 AI 从"辅助工具"变成"自主执行者"时，如何确保它可靠运行？**

在 AI DevOps 中，这体现为 CI/CD 管道中的 AI 质量门禁（自动化代码审查、智能测试选择、根因分析）、AIOps 中的多层验证与自愈机制、以及"人在回路"的审批策略。在 Harness Engineering 中，这体现为六层架构（信息边界、工具系统、执行编排、记忆状态、评估观测、约束恢复）、前馈引导器与反馈传感器的双重控制、以及熵治理和垃圾回收机制。

两者的共同基因可以归纳为四点：约束驱动可靠性（通过限制自由度来提升确定性）、反馈闭环（任何操作都需要验证和纠错）、渐进式信任（从建议模式到自动执行模式的逐步升级）、以及人类监督（高风险操作保留人工审批）。

### 实际的融合

Stripe 的实践是两者融合的最佳案例。他们的 Minions 系统通过 Slack 触发 Agent 写代码、自动过 CI、开 PR，人类仅在 Review 阶段介入，每周合并 1300+ 个 PR。这个系统同时体现了 AI DevOps 的理念（AI 嵌入 CI/CD 流程）和 Harness Engineering 的理念（Blueprint 模式中确定性与概率性节点交替、工具数量控制、升级规则）。Agent 使用与人类工程师相同的 Devbox 和工具链，验证了"对人好的基础设施对 Agent 也好"这一原则。

---

## 第五部分：对"老师的理解"的推测与分析

虽然你没有具体说明老师的观点，但结合"AI DevOps 设计中提到的机制"这一线索，你的老师很可能在讲授以下理念：

在设计 AI DevOps 系统时，关键不是选一个多强的模型，而是设计一套完整的运行控制系统——包括知识如何组织（Context）、行为如何约束（Guardrails）、错误如何检测和恢复（Feedback Loops）、以及长任务中的状态如何管理（Memory）。这些机制的总和，就是 Harness Engineering 所描述的内容。老师可能是在 AI DevOps 的语境下，独立地推导出了与 Harness Engineering 高度一致的工程原则，这恰恰说明了这些原则的普适性——不管你叫它什么名字，在实际构建 AI 系统时都会收敛到类似的解决方案。

---

## 第六部分：Harness Engineering 是否是 AI Agent 的最佳标准？

### 赞成的理由

首先，经验证的实际效果极为亮眼。OpenAI 的 3 人团队 5 个月产出 100 万行代码零手写；Stripe 每周 1300+ PR 合并实现无人值守；独立开发者 Peter Steinberger 一个月 6600+ 次提交，并行运行 5-10 个 Agent。其次，有量化的改进证据：同一模型仅改 Harness，LangChain 成功率从 52.8% 提升到 66.5%，Can.ac 从 6.7% 跳到 68.3%。再者，行业正式认可——AIE Europe 会议开设了世界上第一个 Harness Engineering 专题赛道。

### 反对的理由

技术进步可能使其部分过时。Big Model 阵营的论证有数据支持，推理模型出现后原有的复杂 Agent 系统确实某些部分变得多余。适用范围有限——当前成功案例多在绿地项目（新项目）或基础设施完善的项目中，应用到历史遗留代码库非常困难。核心问题尚未解决——行为验证（代码质量好解决但功能是否正确仍是难题）、编辑合并（Agent 修改代码没有标准可靠方式）、置信度校准（Agent 对幻觉和正确输出表现出同等信心）。成本问题也不可忽视——Anthropic 的三 Agent 框架成本比单 Agent 高 20 倍。

### 综合判断

Harness Engineering 不是永恒的"最佳标准"，而是**当前阶段的最优实践**。它系统性地解决了 Prompt Engineering 和 Context Engineering 无法解决的问题，为 AI Agent 的工业级应用提供了可验证、可复现的工程范式。但它本质上是对当前模型局限性的动态应对——随着模型能力进化，Harness 的内容会持续变化。真正的竞争力不在于搭建多么复杂的 Harness，而在于精准感知模型能力边界并快速做出对应调整的能力。

用一句话总结：**模型决定了系统的上限，Harness 决定了系统的底线。** 在长链路、低容错的商业场景中，与其纠结选哪个模型，不如先把 Harness 搭好。

---

## 结论

AI DevOps 和 Harness Engineering 本质上是同一场范式革命的两个侧面。AI DevOps 从运维和交付的角度切入，关注如何在 CI/CD 管道和生产环境中引入并管理 AI 智能体。Harness Engineering 从开发和工程的角度切入，关注如何为 AI Agent 构建可靠的运行控制系统。二者共享"约束驱动可靠性"的核心基因，在实践中正在快速融合。

Harness Engineering 之所以呈现"哈姆雷特式"的多元解读，根本原因在于它触及了 AI 工程化的深层哲学问题：智能的价值究竟来自模型本身，还是来自围绕模型构建的系统？不同的观察者基于各自的实践经验和利益立场，对同一现象给出了完全不同但各自自洽的解释。这种多元性并非缺陷，而是反映了 AI 工程作为一个年轻学科的本质特征——我们仍在探索最佳实践的过程中，真理很可能在各个极端之间的某个动态平衡点上。

---

## References

1. [一文搞懂 Harness Engineering：六层架构、上下文管理与一线团队实战 | JavaGuide](https://javaguide.cn/ai/agent/harness-engineering.html)
2. [Agent 系列（三）：Harness Engineering | 腾讯云开发者社区](https://cloud.tencent.com/developer/article/2647887)
3. [Harness Engineering（驾驭工程） | 菜鸟教程](https://www.runoob.com/ai-agent/harness-engineering.html)
4. [Harness Engineering 深度解析：Agent 优先时代的软件工程新范式 | 莫尔索](https://liduos.com/agent-engineering/openai-harness-engineering-codex-agent-first)
5. [Harness Engineering：构建高可靠AI Agent的工程方法论 | John's Blog](https://johng.cn/ai/harness-engineering)
6. [Harness Engineering 完全指南 | Bruce AI 工程笔记](https://www.heyuan110.com/zh/posts/ai/2026-03-30-harness-engineering-guide/)
7. [Harness Engineering 实践指南 | Edison's Blog](https://edison-a-n.github.io/2026/03/14/harness-engineering-practical-guide/)
8. [一文读懂 Harness Engineering：从 14 篇工程文章中寻找让 AI 不再离经叛道的壳 | Yousa Driven Development](https://yousali.com/posts/20260405-harness-engineering-guide/)
9. [[AINews] Is Harness Engineering real? | Latent.Space](https://www.latent.space/p/ainews-is-harness-engineering-real)
10. [【译】Harness——用于长时运行应用的智能体框架设计 | 博客园](https://www.cnblogs.com/studyzy/p/19784512)
11. [IDC FutureScape 2026 十大预测：DevOps 正在被重新定义 | IDC](https://www.idc.com/resource-center/blog/idc-futurescape-2026%E5%8D%81%E5%A4%A7%E9%A2%84%E6%B5%8B%EF%BC%9A%E5%BD%93%E6%99%BA%E8%83%BD%E4%BD%93%E8%B5%B0%E8%BF%9B%E5%BC%80%E5%8F%91%E6%B5%81%E7%A8%8B%EF%BC%8Cdevops-%E6%AD%A3%E5%9C%A8%E8%A2%AB/)
12. [AIOps 智能运维体系全景解析 | 腾讯云开发者社区](https://cloud.tencent.com/developer/article/2589477)
13. [将 LLM 深度集成到 CI/CD：自动化代码审查与测试生成 | QubitTool](https://qubittool.com/zh/blog/llm-ci-cd-automated-code-review)
14. [CI/CD in 2025: How AI is Reshaping the Pipeline | Meterra](https://www.meterra.ai/blog/cicd-ai-2025)
15. [Harness Engineering 完全指南：AI Agent 时代的工程新范式 | QubitTool](https://qubittool.com/zh/blog/harness-engineering-complete-guide)
16. [Harness Engineering 从零理解到动手实践 | 博客园](https://www.cnblogs.com/aquester/p/19791985)
17. [Codex + Harness Engineering：OpenAI 如何构建 Agent-First 开发流程 | 掘金](https://juejin.cn/post/7620708166124765220)
18. [AI 驱动的 DevOps：用 AI Agent 自动化 CI/CD、代码审查与运维 | 掘金](https://juejin.cn/post/7618424313797115931)
19. [DevOps & SRE AI Atlas 2026 | GitHub](https://github.com/xdevops-ai/devops-sre-ai-atlas-2025)
20. [Home | Harness Engineering Knowledge Graph](https://harness-engineering.ai/)
