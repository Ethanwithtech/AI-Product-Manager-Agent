# TCCC Desk 在线客服「多场景选择方案」产品策略文档

> **产品经理**：AI PM  
> **日期**：2026-04-01  
> **版本**：v1.0  
> **状态**：Draft  
> **项目仓库**：`TCCC-PC-Demo`

---

## 一、背景与现状分析

### 1.1 产品现状

TCCC PC Demo 是腾讯云联络中心（Tencent Cloud Contact Center）的在线体验演示平台，包含两大产品模块：

| 模块 | 当前能力 | 多场景支持 |
|------|---------|-----------|
| **Voice AI Agent**（语音智能体） | ✅ 已有完善的多场景选择 | 按语言→场景两步配置，V1有3套场景（按语言分），V2有场景+语言+音色三维配置 |
| **Desk Chat AI Agent**（在线智能体） | ❌ 无场景选择能力 | 仅固定的英文落地页 + 单一通用对话流程 |

### 1.2 核心差距

通过代码分析，Voice 模块已具备的场景化能力，Desk 模块完全缺失：

**Voice 已有的场景架构：**
- `VOICE_PERSONAS_V1`：按语言维度定义了 9 个场景（英文3 + 普通话3 + 粤语3）
- 每个场景有独立的 `title`（场景名）、`subtitle`（场景描述）、关联的 `voiceTone`（角色音色）
- V2 版本还有 `SCENES`（客户支持/预约/提醒）+ `VOICE_TONES`（14种音色）+ `LANGUAGES`（12种语言）

**Desk 缺失的部分：**
- `DESK_SUGGESTIONS` 只有3条固定英文建议问题
- `DESK_V1_MENU_ITEMS` 只有4个固定中文菜单
- `renderDeskLanding()` 是单一的通用落地页，无场景差异化
- `renderDeskChatV1()` 和 `renderDeskChatV2()` 的对话流程完全无场景感知
- 对话回复是硬编码的通用回复，不分场景

### 1.3 需求来源

客户明确提出：**想要在 Desk 的在线客服体验部分加上多场景选择方案**。

这与 Voice 模块已有的场景化体验形成了产品一致性要求——用户期望两个产品模块提供同等水平的场景化演示能力。

---

## 二、用户画像与目标

### 2.1 目标用户

| 角色 | 需求 | 痛点 |
|------|------|------|
| **潜在客户/决策者** | 快速评估 Desk 在不同业务场景下的适配性 | 当前只能看到通用演示，无法感知对自己行业/场景的价值 |
| **销售团队** | 针对不同客户演示对应行业场景 | 每次演示都是同一个通用界面，缺乏说服力 |
| **技术评估者** | 了解不同场景下的AI能力差异 | 无法感知多轮对话、知识库、转人工等场景化能力 |

### 2.2 成功指标

| 指标 | 目标 | 衡量方式 |
|------|------|---------|
| 演示完成率 | 从落地页到完整对话 ≥ 60% | 埋点统计 |
| 场景覆盖率 | 用户平均体验 ≥ 2 个场景 | 场景切换统计 |
| 用户停留时长 | Desk 模块停留时长提升 40% | 页面埋点 |
| 试用转化率 | "Start Free Trial" 点击率提升 25% | CTA 按钮埋点 |

---

## 三、场景方案设计

### 3.1 场景矩阵

参考 Voice 模块的场景设计模式（语言维度 × 行业场景），为 Desk 设计以下场景矩阵：

#### 场景定义

| 场景 ID | 场景名称（中） | 场景名称（英） | 图标 | 行业 | 核心演示能力 |
|---------|--------------|--------------|------|------|------------|
| `ecommerce` | 电商购物助手 | E-Commerce Shopping Assistant | 🛒 | 零售/电商 | 商品推荐、订单查询、退换货处理 |
| `finance` | 金融理财顾问 | Financial Advisor | 💰 | 金融 | 账户查询、产品推荐、风险提示 |
| `healthcare` | 医疗健康助手 | Healthcare Assistant | 🏥 | 医疗 | 预约挂号、症状咨询、用药提醒 |
| `travel` | 旅游出行管家 | Travel Concierge | ✈️ | 旅游 | 行程规划、酒店预订、签证咨询 |
| `education` | 教育学习顾问 | Education Advisor | 📚 | 教育 | 课程推荐、学习规划、报名咨询 |
| `tech-support` | 技术支持工程师 | Tech Support Engineer | 🔧 | IT/SaaS | 故障排查、产品引导、工单创建 |

#### 语言维度

每个场景支持以下语言变体（与 Voice 保持一致）：

- **英语（en）**：默认
- **简体中文（zh-CN）**：核心
- **繁体中文/粤语（zh-TW）**：港澳台

### 3.2 每个场景的差异化元素

```
Desk Scene = {
  id: string,                    // 场景唯一标识
  title: { en, zh },             // 场景标题
  subtitle: { en, zh },          // 场景描述
  icon: string,                  // 场景图标
  welcomeMessage: { en, zh },    // AI 首次打招呼内容
  suggestions: { en, zh }[],     // 3条场景化快捷建议
  sampleConversation: Message[], // 预设的场景化对话流程
  botAvatar: string,             // 场景专属头像
  botName: { en, zh },           // 场景专属 Bot 名称
  brandColor: string,            // 场景主题色（可选）
  landingImage: string,          // 落地页背景图
  menuItems: MenuItem[],         // V1 底部菜单项
}
```

### 3.3 交互流程设计

#### 方案 A：左侧配置面板（推荐 ⭐）

参考 Voice 模块的 `renderVoiceConfigPanelV1()` 设计模式：

```
┌──────────┬─────────────────────────────────┐
│ 配置面板  │                                 │
│          │                                 │
│ ① 语言   │      Desk Chat 窗口             │
│  English │      （根据场景动态变化）         │
│  中文    │                                 │
│  粤语    │                                 │
│          │                                 │
│ ② 场景   │                                 │
│  🛒 电商  │                                 │
│  💰 金融  │                                 │
│  🏥 医疗  │                                 │
│  ✈️ 旅游  │                                 │
│  📚 教育  │                                 │
│  🔧 技术  │                                 │
│          │                                 │
│ [折叠 <] │                                 │
└──────────┴─────────────────────────────────┘
```

**优势**：
- 与 Voice V1 的交互模式完全一致，用户无需学习新交互
- 可折叠，不遮挡聊天窗口
- 切换场景时可实时看到聊天窗口内容变化

#### 方案 B：聊天窗口内卡片选择

在落地页直接将 3 个固定建议替换为场景卡片：

```
┌─────────────────────────────────┐
│        Desk Chat AI Agent       │
│                                 │
│   [AI头像] 欢迎！请选择场景：    │
│                                 │
│   ┌─────────┐ ┌─────────┐      │
│   │ 🛒 电商  │ │ 💰 金融  │      │
│   └─────────┘ └─────────┘      │
│   ┌─────────┐ ┌─────────┐      │
│   │ 🏥 医疗  │ │ ✈️ 旅游  │      │
│   └─────────┘ └─────────┘      │
│                                 │
│   [输入框]              [发送]  │
└─────────────────────────────────┘
```

**优势**：
- 沉浸式体验，不需要额外面板
- 移动端友好
- 用户可快速进入场景

#### 推荐决策：**方案 A + 方案 B 结合**

- **V1 模式**：使用方案 B（卡片选择），保持 V1 移动端沉浸式风格
- **V2 模式**：使用方案 A（左侧面板），与 Voice V2 的配置面板风格统一

---

## 四、技术方案设计

### 4.1 数据结构变更

#### `types.ts` 新增

```typescript
// 新增 Desk 场景类型
export type DeskSceneType = 
  | 'ecommerce' 
  | 'finance' 
  | 'healthcare' 
  | 'travel' 
  | 'education' 
  | 'tech-support' 
  | null;

// 在 AppState 中添加
export interface AppState {
  // ... existing fields
  deskScene: DeskSceneType;  // 新增：Desk 场景选择
}
```

#### `constants.ts` 新增

```typescript
// Desk 场景配置
export const DESK_SCENES: {
  id: DeskSceneType;
  icon: string;
  title: { en: string; zh: string };
  subtitle: { en: string; zh: string };
  welcomeMessage: { en: string; zh: string };
  suggestions: { en: string[]; zh: string[] };
  botName: { en: string; zh: string };
  sampleResponses: Record<string, { en: string; zh: string }>;
}[] = [
  {
    id: 'ecommerce',
    icon: '🛒',
    title: { en: 'E-Commerce Assistant', zh: '电商购物助手' },
    subtitle: { 
      en: 'Product recommendations, order tracking & returns', 
      zh: '商品推荐、订单跟踪、退换货处理' 
    },
    welcomeMessage: {
      en: "Welcome to ShopSmart! I'm your AI shopping assistant. How can I help you today?",
      zh: "欢迎来到智慧商城！我是您的AI购物助手，请问有什么可以帮您？"
    },
    suggestions: {
      en: [
        "I want to track my order #12345",
        "Recommend a laptop under $1000",
        "How do I return a product?"
      ],
      zh: [
        "我想查询订单 #12345 的物流状态",
        "推荐一款1000元以内的蓝牙耳机",
        "如何申请退换货？"
      ]
    },
    botName: { en: 'ShopBot', zh: '购物助手' },
    sampleResponses: { /* 场景化回复映射 */ }
  },
  // ... 其他场景
];

// V1 专用：按语言分组的 Desk 场景（类似 VOICE_PERSONAS_V1）
export const DESK_PERSONAS_V1: Record<string, {
  id: DeskSceneType;
  title: { en: string; zh: string };
  subtitle: { en: string; zh: string };
}[]> = {
  'en': [
    {
      id: 'ecommerce',
      title: { en: 'E-Commerce Assistant', zh: '电商购物助手' },
      subtitle: { 
        en: 'Product recommendations, order tracking & return processing.',
        zh: '商品推荐、订单跟踪和退换货处理。'
      }
    },
    {
      id: 'tech-support',
      title: { en: 'Tech Support Helpdesk', zh: '技术支持工程师' },
      subtitle: {
        en: 'Troubleshooting, product guidance, and ticket creation.',
        zh: '故障排查、产品引导和工单创建。'
      }
    },
    {
      id: 'travel',
      title: { en: 'Travel Concierge', zh: '旅游出行管家' },
      subtitle: {
        en: 'Trip planning, hotel booking, and visa inquiries.',
        zh: '行程规划、酒店预订和签证咨询。'
      }
    },
  ],
  'zh-CN': [
    {
      id: 'ecommerce',
      title: { en: 'Smart Shopping Assistant', zh: '智慧购物助手' },
      subtitle: {
        en: 'AI-powered shopping experience with smart recommendations.',
        zh: 'AI驱动的购物体验，智能商品推荐与售后服务。'
      }
    },
    {
      id: 'finance',
      title: { en: 'Financial Advisory Bot', zh: '智能理财顾问' },
      subtitle: {
        en: 'Account inquiries, product recommendations, and risk alerts.',
        zh: '账户查询、理财产品推荐、风险提示。'
      }
    },
    {
      id: 'healthcare',
      title: { en: 'Health Consultation Assistant', zh: '健康咨询助手' },
      subtitle: {
        en: 'Appointment booking, symptom consultation, medication reminders.',
        zh: '预约挂号、症状咨询、用药提醒。'
      }
    },
  ],
  'zh-TW': [
    {
      id: 'finance',
      title: { en: 'Banking Service Bot', zh: '银行服务机器人' },
      subtitle: {
        en: 'Account balance, transfer, and credit card inquiries.',
        zh: '账户余额、转账和信用卡查询服务。'
      }
    },
    {
      id: 'travel',
      title: { en: 'HK Travel Concierge', zh: '港澳旅游管家' },
      subtitle: {
        en: 'Local attractions, dining, and transport recommendations.',
        zh: '本地景点、美食和交通推荐。'
      }
    },
    {
      id: 'education',
      title: { en: 'Course Advisor', zh: '课程顾问' },
      subtitle: {
        en: 'Course recommendations, enrollment, and learning plans.',
        zh: '课程推荐、报名咨询和学习规划。'
      }
    },
  ]
};
```

### 4.2 组件变更

#### 需要修改的文件

| 文件 | 变更内容 | 优先级 |
|------|---------|--------|
| `types.ts` | 新增 `DeskSceneType`，`AppState` 增加 `deskScene` 字段 | P0 |
| `constants.ts` | 新增 `DESK_SCENES`、`DESK_PERSONAS_V1`、场景化建议和回复 | P0 |
| `App.tsx` - state | 初始化 `deskScene` 状态 | P0 |
| `App.tsx` - `renderDeskLanding()` | 落地页添加场景选择卡片，建议文案根据场景变化 | P0 |
| `App.tsx` - `renderDeskChatV1()` | V1 聊天界面：欢迎语、建议、回复根据场景变化 | P0 |
| `App.tsx` - `renderDeskChatV2()` | V2 聊天界面：同上 | P0 |
| `App.tsx` - 新增 `renderDeskConfigPanel()` | V2 模式下的左侧场景配置面板 | P1 |
| `App.tsx` - `startDeskChat()` | 根据选中场景生成不同欢迎语 | P0 |
| `App.tsx` - `handleSendMessage()` | 根据场景返回不同的模拟回复 | P1 |
| `App.tsx` - `streamDeskResponse()` | 支持场景化回复内容 | P1 |

### 4.3 关键交互变更

#### 4.3.1 落地页场景入口（`renderDeskLanding` 改造）

**现在的实现**（`App.tsx` 第 704-721 行）：
```tsx
// 当前：3个固定建议
{DESK_SUGGESTIONS.slice(0, 3).map((q, idx) => (
  <button key={idx} onClick={() => startDeskChat(q)} ...>
    <span>{q}</span>
  </button>
))}
```

**改造后**：
```tsx
// 改造：场景选择卡片 + 场景化建议
{currentDeskScenes.map((scene, idx) => (
  <button 
    key={idx} 
    onClick={() => {
      setState(p => ({...p, deskScene: scene.id}));
      startDeskChat(); // 进入场景化对话
    }}
    className="scene-card ..."
  >
    <span className="scene-icon">{scene.icon}</span>
    <div>
      <span className="scene-title">{scene.title[uiLang]}</span>
      <span className="scene-subtitle">{scene.subtitle[uiLang]}</span>
    </div>
  </button>
))}
```

#### 4.3.2 V1 聊天界面场景化（`renderDeskChatV1` 改造）

**欢迎语变化**（当前是硬编码中文，第 761-763 行）：
```tsx
// 当前
<p className="font-bold mb-3">您好，欢迎咨询Desk智能客服！</p>
<p className="mb-3 text-gray-600">我是小Desk...</p>

// 改造后：根据 deskScene 动态显示
const scene = DESK_SCENES.find(s => s.id === state.deskScene);
<p className="font-bold mb-3">{scene.welcomeMessage[uiLang]}</p>
```

**底部菜单变化**（当前是固定菜单，第 812-821 行）：
```tsx
// 改造后：根据场景动态显示菜单
const sceneMenuItems = scene?.menuItems || DESK_V1_MENU_ITEMS;
```

#### 4.3.3 V2 配置面板（新增 `renderDeskConfigPanel`）

新增一个与 Voice 的 `renderVoiceConfigPanel()` 结构相同的面板，包含：
- Step 1：语言选择
- Step 2：场景选择（卡片列表）

### 4.4 对话流程场景化

#### 模拟回复逻辑改造

当前 `handleSendMessage()` 返回固定回复：
```tsx
// 当前（第 225 行）
const responseText = "AI Agent: Analyzing your request...";
```

改造为场景化回复引擎：

```typescript
const getSceneResponse = (scene: DeskSceneType, userInput: string, lang: LangType): string => {
  const responses = DESK_SCENE_RESPONSES[scene || 'ecommerce'];
  
  // 简单关键词匹配
  const keywords = Object.keys(responses);
  const matched = keywords.find(kw => 
    userInput.toLowerCase().includes(kw.toLowerCase())
  );
  
  if (matched) {
    return responses[matched][lang === 'zh-CN' ? 'zh' : 'en'];
  }
  
  // 默认场景化回复
  return responses['default'][lang === 'zh-CN' ? 'zh' : 'en'];
};
```

---

## 五、场景化内容示例

### 5.1 电商购物助手 🛒

| 元素 | 英文 | 中文 |
|------|------|------|
| 欢迎语 | "Welcome to ShopSmart! I can help you track orders, find products, or process returns." | "欢迎来到智慧商城！我可以帮您查询订单、推荐商品或处理退换货。" |
| 建议1 | "Track my order #12345" | "查询订单物流状态" |
| 建议2 | "Recommend a laptop under $1000" | "推荐1000元以内的蓝牙耳机" |
| 建议3 | "How to return a product?" | "如何申请退换货？" |
| 示例回复 | "I found your order #12345. It's currently in transit and expected to arrive on April 3rd. Would you like me to set up a delivery notification?" | "已查询到您的订单 #12345，目前包裹正在运输中，预计4月3日送达。需要我为您设置到货提醒吗？" |

### 5.2 金融理财顾问 💰

| 元素 | 英文 | 中文 |
|------|------|------|
| 欢迎语 | "Hello! I'm your AI Financial Advisor. How can I assist you with your banking needs today?" | "您好！我是您的AI理财顾问。今天有什么银行业务需要帮您处理？" |
| 建议1 | "Check my account balance" | "查询账户余额" |
| 建议2 | "What savings products do you offer?" | "有哪些理财产品推荐？" |
| 建议3 | "Report a suspicious transaction" | "挂失银行卡" |

### 5.3 医疗健康助手 🏥

| 元素 | 英文 | 中文 |
|------|------|------|
| 欢迎语 | "Welcome to HealthCare Plus! I can help you book appointments, check symptoms, or manage prescriptions." | "欢迎来到健康+！我可以帮您预约挂号、查询症状或管理用药。" |
| 建议1 | "Book an appointment with Dr. Smith" | "预约明天上午的内科门诊" |
| 建议2 | "I've been having headaches lately" | "最近经常头疼怎么办？" |
| 建议3 | "Remind me about my medication" | "帮我设置用药提醒" |

### 5.4 旅游出行管家 ✈️

| 元素 | 英文 | 中文 |
|------|------|------|
| 欢迎语 | "Hi there! I'm your Travel Concierge. Let me help you plan the perfect trip!" | "您好！我是您的旅游管家，让我帮您规划完美行程！" |
| 建议1 | "Plan a 5-day trip to Tokyo" | "帮我规划5天东京行程" |
| 建议2 | "Find hotels near Times Square" | "推荐三亚海景酒店" |
| 建议3 | "Do I need a visa for Thailand?" | "去泰国需要签证吗？" |

### 5.5 教育学习顾问 📚

| 元素 | 英文 | 中文 |
|------|------|------|
| 欢迎语 | "Welcome to EduPro! I'm here to help you find the perfect learning path." | "欢迎来到智学！我来帮您找到最适合的学习路径。" |
| 建议1 | "What Python courses do you recommend?" | "推荐入门级Python课程" |
| 建议2 | "How do I enroll in the MBA program?" | "MBA报名流程是怎样的？" |
| 建议3 | "Create a study plan for IELTS" | "帮我制定雅思学习计划" |

### 5.6 技术支持工程师 🔧

| 元素 | 英文 | 中文 |
|------|------|------|
| 欢迎语 | "Hello! I'm your Tech Support Engineer. Describe your issue and I'll help resolve it." | "您好！我是技术支持工程师。请描述您遇到的问题，我来帮您解决。" |
| 建议1 | "My app keeps crashing on login" | "应用登录时一直闪退" |
| 建议2 | "How do I reset my API key?" | "如何重置API密钥？" |
| 建议3 | "Create a support ticket" | "提交工单" |

---

## 六、V1 vs V2 差异化设计

### V1（演示版）—— 沉浸式场景卡片

```
┌─────────────────────────────────┐
│     Hi, 我是 Desk 智能客服       │   ← 场景化 Bot 名称
│                                 │
│  [Bot头像] 欢迎！请选择场景体验：  │   ← 场景化欢迎语
│                                 │
│  ┌────────────────────────────┐ │
│  │ 🛒 电商购物助手              │ │   ← 场景卡片（可滑动）
│  │ 商品推荐、订单跟踪、退换货    │ │
│  └────────────────────────────┘ │
│  ┌────────────────────────────┐ │
│  │ 💰 智能理财顾问              │ │
│  │ 账户查询、产品推荐、风险提示  │ │
│  └────────────────────────────┘ │
│  ┌────────────────────────────┐ │
│  │ 🏥 健康咨询助手              │ │
│  │ 预约挂号、症状咨询、用药提醒  │ │
│  └────────────────────────────┘ │
│                                 │
│  ┌─────────────────────┐[发送]  │
│  │ 请输入消息            │       │
│  └─────────────────────┘       │
└─────────────────────────────────┘
```

### V2（线上版）—— 左侧配置面板 + 精致聊天窗口

```
┌──────────┬────────────────────────────────┐
│ ⚙ 设置   │                                │
│          │     Desk Chat AI Agent         │
│ ① 语言   │                                │
│  ● English│  [落地页内容 - 根据场景变化]     │
│  ○ 中文   │                                │
│  ○ 粤语   │  "Welcome to ShopSmart!"       │
│          │                                │
│ ② 场景   │  ┌──────────────────────────┐   │
│          │  │ Track my order #12345    │   │
│ ● 🛒 电商 │  └──────────────────────────┘   │
│ ○ 💰 金融 │  ┌──────────────────────────┐   │
│ ○ 🏥 医疗 │  │ Recommend a laptop       │   │
│ ○ ✈️ 旅游 │  └──────────────────────────┘   │
│ ○ 📚 教育 │                                │
│ ○ 🔧 技术 │  [输入框]              [发送]   │
│ [< 折叠]  │                                │
└──────────┴────────────────────────────────┘
```

---

## 七、实施计划

### Phase 1：核心数据与类型（1天）

- [ ] `types.ts`：新增 `DeskSceneType`
- [ ] `types.ts`：`AppState` 添加 `deskScene` 字段
- [ ] `constants.ts`：新增 `DESK_SCENES` 全场景配置
- [ ] `constants.ts`：新增 `DESK_PERSONAS_V1`（按语言分组）
- [ ] `constants.ts`：新增每个场景的 `suggestions`、`welcomeMessage`、`sampleResponses`

### Phase 2：V1 场景化改造（2天）

- [ ] `App.tsx`：state 初始化增加 `deskScene`
- [ ] `renderDeskLanding()`：落地页建议区域改为场景选择卡片
- [ ] `renderDeskChatV1()`：欢迎语根据场景动态显示
- [ ] `renderDeskChatV1()`：底部建议根据场景变化
- [ ] `startDeskChat()`：根据场景生成欢迎语
- [ ] `handleSendMessage()`：根据场景返回场景化回复

### Phase 3：V2 配置面板（2天）

- [ ] 新增 `renderDeskConfigPanel()`：左侧语言+场景配置面板
- [ ] `renderDeskLanding()`：V2 模式下落地页内容根据场景变化
- [ ] `renderDeskChatV2()`：聊天界面根据场景变化
- [ ] 面板折叠/展开动画

### Phase 4：对话体验优化（1天）

- [ ] 实现场景化回复引擎 `getSceneResponse()`
- [ ] 每个场景至少 5 组关键词-回复映射
- [ ] 场景切换时重置对话
- [ ] 转人工文案场景化

### Phase 5：多语言完善与测试（1天）

- [ ] 所有场景的中英文翻译完善
- [ ] 粤语场景适配
- [ ] `TRANSLATIONS` 新增场景相关 UI 翻译
- [ ] 全场景手动测试

---

## 八、风险与注意事项

### 8.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| App.tsx 文件过大（已 1100+ 行） | 维护困难 | 考虑将 Desk 相关渲染逻辑抽取为独立组件 `DeskDemo.tsx` |
| 场景回复过于简单 | 体验不真实 | 每个场景准备 10+ 组关键词映射，覆盖常见问题 |
| 语言切换时场景不同步 | 用户困惑 | 切换语言时自动匹配对应语言的默认场景 |

### 8.2 产品风险

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 场景过多导致选择困难 | 降低转化 | 每种语言只展示 3 个场景（与 Voice 保持一致） |
| 场景演示与真实能力差距 | 期望管理 | 在场景描述中明确标注"演示场景" |
| V1/V2 体验割裂 | 产品一致性 | 核心场景数据共享，只在交互形式上差异化 |

### 8.3 反模式警告

> ⚠️ **不要做的事：**
> 1. **不要** 给每个场景做完全独立的聊天组件 —— 应复用现有 `renderDeskChatV1/V2`，通过数据驱动差异化
> 2. **不要** 让场景选择成为必选项 —— 保留直接输入的路径，用户可以跳过场景选择直接开聊
> 3. **不要** 在 V1 中加配置面板 —— V1 是移动端模拟器，空间有限，用卡片式选择
> 4. **不要** 把场景逻辑硬编码在组件里 —— 全部放 `constants.ts`，保持数据驱动

---

## 九、与 Voice 模块的对齐清单

确保 Desk 多场景与 Voice 多场景体验一致性：

| 维度 | Voice 现状 | Desk 目标 | 对齐状态 |
|------|-----------|----------|---------|
| 场景数量/语言 | 3个/语言 | 3个/语言 | ✅ |
| 配置入口（V1） | 左侧面板 Step1+Step2 | 聊天窗口内卡片选择 | 🔄 差异化但合理 |
| 配置入口（V2） | 左侧面板 Scene+Lang+Tone | 左侧面板 Lang+Scene | ✅ |
| 场景数据结构 | `VOICE_PERSONAS_V1` | `DESK_PERSONAS_V1` | ✅ |
| 多语言支持 | en/zh-CN/zh-TW | en/zh-CN/zh-TW | ✅ |
| 场景切换重置 | 重新开始语音交互 | 重新开始聊天 | ✅ |

---

## 十、总结

本方案的核心思路是：**以 Voice 模块已有的场景化架构为蓝本，为 Desk 在线客服模块补齐多场景选择能力，实现两大产品模块的体验一致性。**

关键设计决策：
1. **数据驱动**：所有场景差异化通过 `constants.ts` 配置实现，不改变组件结构
2. **V1/V2 差异化交互**：V1 用卡片选择（适配移动端），V2 用面板选择（适配桌面端）
3. **3×3 场景矩阵**：每种语言 3 个行业场景，总共 9 个场景变体
4. **渐进式实施**：5个 Phase，约 7 个工作日完成全部功能

---

*本文档由产品经理基于代码库分析和客户需求制定，如需修改请反馈。*
