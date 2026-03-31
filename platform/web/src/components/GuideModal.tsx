import React, { useState, useEffect } from 'react';
import { Modal, Button, Space, Typography, Steps, Tag, Divider } from '@arco-design/web-react';
import {
  IconBook, IconFile, IconDashboard, IconSettings,
  IconBulb, IconRight, IconLeft, IconCheckCircleFill,
  IconRobot, IconApps,
} from '@arco-design/web-react/icon';

const { Title, Text, Paragraph } = Typography;
const Step = Steps.Step;

const GUIDE_KEY = 'pm-team-hub-guide-shown';

interface GuideStep {
  title: string;
  icon: React.ReactNode;
  content: React.ReactNode;
}

const GuideModal: React.FC = () => {
  const [visible, setVisible] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const shown = localStorage.getItem(GUIDE_KEY);
    if (!shown) {
      // 首次访问时延迟500ms弹出
      const timer = setTimeout(() => setVisible(true), 500);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleClose = () => {
    setVisible(false);
    localStorage.setItem(GUIDE_KEY, 'true');
  };

  const handleRestart = () => {
    setCurrentStep(0);
    setVisible(true);
  };

  const steps: GuideStep[] = [
    {
      title: '欢迎来到 PM Team Hub 👋',
      icon: <IconApps style={{ fontSize: 32, color: '#165DFF' }} />,
      content: (
        <div>
          <Paragraph className="text-base leading-relaxed">
            PM Team Hub 是为你的<strong>产品团队</strong>设计的 AI 协作平台。它通过三层架构让你和团队高效工作：
          </Paragraph>
          <div className="grid grid-cols-1 gap-3 mt-4">
            <div className="flex items-start gap-3 p-3 rounded-lg" style={{ background: '#F0F5FF' }}>
              <span className="text-xl">🧠</span>
              <div>
                <Text className="font-medium block">AI Skills（在你的 CodeBuddy 中）</Text>
                <Text type="secondary" className="text-sm">每个 PM 在自己的 CodeBuddy 中加载 Skills，AI 帮你写需求、生成 UI 稿、同步进度</Text>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 rounded-lg" style={{ background: '#E8F3FF' }}>
              <span className="text-xl">🔗</span>
              <div>
                <Text className="font-medium block">MCP Server（共享数据中心）</Text>
                <Text type="secondary" className="text-sm">所有 PM 的 CodeBuddy 连接同一个 MCP Server，共享知识库、需求单和进度</Text>
              </div>
            </div>
            <div className="flex items-start gap-3 p-3 rounded-lg" style={{ background: '#FFF7E8' }}>
              <span className="text-xl">💻</span>
              <div>
                <Text className="font-medium block">管理台（你现在看到的）</Text>
                <Text type="secondary" className="text-sm">浏览器中管理共享数据——查看和编辑知识库、需求单、进度看板、规则模板</Text>
              </div>
            </div>
          </div>
        </div>
      ),
    },
    {
      title: '第一步：配置 CodeBuddy 🔧',
      icon: <IconRobot style={{ fontSize: 32, color: '#722ED1' }} />,
      content: (
        <div>
          <Paragraph className="text-base leading-relaxed">
            让你的 CodeBuddy 连接到这个 MCP Server，就能在对话中直接操作共享数据。
          </Paragraph>
          <div className="mt-3 p-4 rounded-lg" style={{ background: '#1D2129', color: '#E5E6EB' }}>
            <Text className="text-xs block mb-2" style={{ color: '#86909C' }}>CodeBuddy MCP 配置（添加到你的 MCP 设置中）</Text>
            <pre className="text-sm" style={{ color: '#E5E6EB', margin: 0, whiteSpace: 'pre-wrap' }}>
{`{
  "mcpServers": {
    "pm-team-hub": {
      "url": "http://<服务器IP>:8000/mcp",
      "description": "PM团队共享数据中心"
    }
  }
}`}
            </pre>
          </div>
          <div className="mt-4 p-3 rounded-lg" style={{ background: '#E8FFEA' }}>
            <Text className="text-sm">
              <IconBulb className="mr-1" style={{ color: '#00B42A' }} />
              <strong>提示：</strong>将 <code>&lt;服务器IP&gt;</code> 替换为部署了 MCP Server 的实际地址。
              如果是团队内网，所有人使用同一个地址。
            </Text>
          </div>
        </div>
      ),
    },
    {
      title: '知识库管理 📚',
      icon: <IconBook style={{ fontSize: 32, color: '#165DFF' }} />,
      content: (
        <div>
          <Paragraph className="text-base leading-relaxed">
            知识库是 AI 的「记忆」。上传你的产品文档后，AI 在写需求、生成 UI 时会自动检索相关内容。系统内置 <strong>ChromaDB 向量数据库</strong>，上传即自动分块、嵌入、索引。
          </Paragraph>
          <Divider className="my-3" />
          <div className="space-y-3">
            <div className="flex items-start gap-2">
              <Tag color="arcoblue" size="small">支持格式</Tag>
              <Text className="text-sm">Markdown (.md)、纯文本 (.txt)、<strong>PDF (.pdf)</strong>、<strong>Word (.docx)</strong>、HTML (.html) — 拖拽上传自动解析</Text>
            </div>
            <div className="flex items-start gap-2">
              <Tag color="green" size="small">推荐上传</Tag>
              <Text className="text-sm">IM/TCCC 产品文档、竞品分析、用户调研报告、技术方案、接口文档</Text>
            </div>
            <div className="flex items-start gap-2">
              <Tag color="orange" size="small">检索测试</Tag>
              <Text className="text-sm">
                上传后点击「检索测试」，输入自然语言查询验证效果。相关度分数越接近 1 越好。
              </Text>
            </div>
            <div className="flex items-start gap-2">
              <Tag color="purple" size="small">MCP 工具</Tag>
              <Text className="text-sm">
                在 CodeBuddy 中可用 <code>search_knowledge</code>、<code>add_knowledge_document</code> 等 4 个 MCP 工具直接操作知识库。
              </Text>
            </div>
          </div>
        </div>
      ),
    },
    {
      title: '需求单管理 📝',
      icon: <IconFile style={{ fontSize: 32, color: '#FF7D00' }} />,
      content: (
        <div>
          <Paragraph className="text-base leading-relaxed">
            需求单由 AI 在 CodeBuddy 中生成，自动存储到 MCP Server，你可以在这里浏览、编辑和管理。还可以 <strong>一键同步到 TAPD</strong>。
          </Paragraph>
          <Divider className="my-3" />
          <div className="space-y-3">
            <div className="flex items-start gap-2">
              <span className="text-lg">1️⃣</span>
              <div>
                <Text className="font-medium text-sm">在 CodeBuddy 中生成</Text>
                <Text type="secondary" className="text-sm block">
                  使用 <code>/generate-requirement</code> 命令，AI 先检索知识库 → 读取模板 → 生成 PRD → 检查冲突
                </Text>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-lg">2️⃣</span>
              <div>
                <Text className="font-medium text-sm">在管理台查看和编辑</Text>
                <Text type="secondary" className="text-sm block">点击卡片打开详情，支持 Markdown 预览和编辑，可以调整状态</Text>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-lg">3️⃣</span>
              <div>
                <Text className="font-medium text-sm">同步到 TAPD（可选）</Text>
                <Text type="secondary" className="text-sm block">
                  PRD 生成后可一键同步：在 TAPD 创建需求 → 上传 PRD 附件 → 嵌入架构图。需先配置 <code>~/.tapd/credentials</code>
                </Text>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <span className="text-lg">4️⃣</span>
              <div>
                <Text className="font-medium text-sm">状态流转</Text>
                <Text type="secondary" className="text-sm block">
                  草稿 → 评审中 → 已通过 → 已归档，支持按状态和作者筛选
                </Text>
              </div>
            </div>
          </div>
        </div>
      ),
    },
    {
      title: '进度看板 📊',
      icon: <IconDashboard style={{ fontSize: 32, color: '#722ED1' }} />,
      content: (
        <div>
          <Paragraph className="text-base leading-relaxed">
            看板展示所有 PM 的工作进度，<strong>自动检测冲突</strong>（两人修改同一模块或关键词重叠过多时会预警）。
          </Paragraph>
          <Divider className="my-3" />
          <div className="grid grid-cols-4 gap-2 mb-4">
            {[
              { label: '📋 规划中', bg: '#F0F5FF', color: '#165DFF' },
              { label: '🔨 进行中', bg: '#FFF7E8', color: '#FF7D00' },
              { label: '🔍 评审中', bg: '#F5E8FF', color: '#722ED1' },
              { label: '✅ 已完成', bg: '#E8FFEA', color: '#00B42A' },
            ].map((col) => (
              <div key={col.label} className="text-center p-2 rounded-lg text-xs font-medium"
                style={{ background: col.bg, color: col.color }}>
                {col.label}
              </div>
            ))}
          </div>
          <div className="p-3 rounded-lg" style={{ background: '#FFF0F0' }}>
            <Text className="text-sm">
              <strong>⚠️ 冲突检测：</strong>点击任意卡片查看详情时，系统会自动检查该项是否与其他 PM 的工作有模块重叠。
              发现冲突时会显示红色提示和协调建议。
            </Text>
          </div>
        </div>
      ),
    },
    {
      title: '规则与模板 📋',
      icon: <IconSettings style={{ fontSize: 32, color: '#00B42A' }} />,
      content: (
        <div>
          <Paragraph className="text-base leading-relaxed">
            团队共享的 PRD 模板、检查清单和规范规则。AI 在生成需求时会自动调用 <code>get_templates</code> 读取这些模板。
          </Paragraph>
          <Divider className="my-3" />
          <div className="space-y-3">
            <div className="flex items-start gap-2">
              <Tag color="arcoblue" size="small">需求模板</Tag>
              <Text className="text-sm">标准 PRD 结构模板，包含背景、目标、功能需求、里程碑等章节</Text>
            </div>
            <div className="flex items-start gap-2">
              <Tag color="green" size="small">检查清单</Tag>
              <Text className="text-sm">Sprint 评审、上线检查等可勾选的检查项</Text>
            </div>
            <div className="flex items-start gap-2">
              <Tag color="orange" size="small">团队规则</Tag>
              <Text className="text-sm">命名规范、优先级定义、状态流转规则等</Text>
            </div>
          </div>
          <div className="mt-4 p-3 rounded-lg" style={{ background: '#E8F3FF' }}>
            <Text className="text-sm">
              <IconBulb className="mr-1" style={{ color: '#165DFF' }} />
              <strong>两种创建方式：</strong>① 点击「新建模板」手动编写 Markdown ② 点击「上传模板文件」导入 .md/.txt/.docx/.pdf 文件，内容自动解析为模板。
            </Text>
          </div>
        </div>
      ),
    },
    {
      title: '推荐工作流 🚀',
      icon: <IconCheckCircleFill style={{ fontSize: 32, color: '#00B42A' }} />,
      content: (
        <div>
          <Paragraph className="text-base leading-relaxed">
            以下是推荐的日常工作流程，帮你最大化利用 AI：
          </Paragraph>
          <div className="space-y-3 mt-4">
            <div className="p-3 rounded-lg border-l-4" style={{ background: '#F0F5FF', borderColor: '#165DFF' }}>
              <Text className="font-medium block mb-1">🌅 早上：同步进度</Text>
              <Text type="secondary" className="text-sm">
                在 CodeBuddy 中运行 <code>product-sync-agent</code> skill，更新你的工作状态，检查冲突
              </Text>
            </div>
            <div className="p-3 rounded-lg border-l-4" style={{ background: '#FFF7E8', borderColor: '#FF7D00' }}>
              <Text className="font-medium block mb-1">📝 写需求时：一键生成 + TAPD 同步</Text>
              <Text type="secondary" className="text-sm">
                使用 <code>/generate-requirement</code> → 检索知识库 → 套用模板 → 生成 PRD → 同步 TAPD → 自动检测冲突
              </Text>
            </div>
            <div className="p-3 rounded-lg border-l-4" style={{ background: '#FFF0F0', borderColor: '#F53F3F' }}>
              <Text className="font-medium block mb-1">💬 收到反馈时：AI 分析</Text>
              <Text type="secondary" className="text-sm">
                使用 <code>feedback-insight-engine</code> skill，导入标书/评论/访谈数据，AI 提取主题、评估影响、推荐迭代方向
              </Text>
            </div>
            <div className="p-3 rounded-lg border-l-4" style={{ background: '#F5E8FF', borderColor: '#722ED1' }}>
              <Text className="font-medium block mb-1">🎨 出 UI 稿时：快速原型</Text>
              <Text type="secondary" className="text-sm">
                使用 <code>/generate-ui-draft</code> 命令，AI 基于需求生成 React + Arco Design 代码
              </Text>
            </div>
            <div className="p-3 rounded-lg border-l-4" style={{ background: '#E8FFEA', borderColor: '#00B42A' }}>
              <Text className="font-medium block mb-1">⚡ 全链路：需求到 UI 一步到位</Text>
              <Text type="secondary" className="text-sm">
                使用 <code>/fullchain</code> 命令，从知识检索到 PRD 到 UI 稿到团队同步，全自动完成
              </Text>
            </div>
          </div>
        </div>
      ),
    },
  ];

  return (
    <>
      {/* 引导按钮 — 固定在右下角 */}
      <div
        className="fixed bottom-6 right-6 z-50 cursor-pointer"
        onClick={handleRestart}
        title="查看使用引导"
      >
        <div className="w-12 h-12 rounded-full flex items-center justify-center shadow-lg hover:shadow-xl transition-shadow"
          style={{ background: 'linear-gradient(135deg, #165DFF 0%, #0E42D2 100%)' }}>
          <IconBulb style={{ fontSize: 22, color: '#fff' }} />
        </div>
      </div>

      <Modal
        visible={visible}
        onCancel={handleClose}
        footer={null}
        style={{ width: 680 }}
        closable={true}
        maskClosable={false}
        unmountOnExit
      >
        <div className="px-2">
          {/* Step indicator */}
          <Steps current={currentStep} size="small" className="mb-6" style={{ padding: '0 20px' }}>
            {steps.map((s, i) => (
              <Step key={i} />
            ))}
          </Steps>

          {/* Step content */}
          <div className="flex items-start gap-4 mb-6">
            <div className="flex-shrink-0 mt-1">
              {steps[currentStep].icon}
            </div>
            <div className="flex-1">
              <Title heading={5} style={{ margin: '0 0 12px 0' }}>
                {steps[currentStep].title}
              </Title>
              {steps[currentStep].content}
            </div>
          </div>

          <Divider className="my-4" />

          {/* Navigation */}
          <div className="flex items-center justify-between">
            <Text type="secondary" className="text-sm">
              {currentStep + 1} / {steps.length}
            </Text>
            <Space>
              {currentStep > 0 && (
                <Button
                  icon={<IconLeft />}
                  onClick={() => setCurrentStep(currentStep - 1)}
                >
                  上一步
                </Button>
              )}
              {currentStep < steps.length - 1 ? (
                <Button
                  type="primary"
                  onClick={() => setCurrentStep(currentStep + 1)}
                >
                  下一步 <IconRight className="ml-1" />
                </Button>
              ) : (
                <Button
                  type="primary"
                  status="success"
                  onClick={handleClose}
                >
                  <IconCheckCircleFill className="mr-1" /> 开始使用
                </Button>
              )}
            </Space>
          </div>
        </div>
      </Modal>
    </>
  );
};

export default GuideModal;
