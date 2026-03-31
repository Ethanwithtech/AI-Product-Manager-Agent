import React, { useState, useEffect } from 'react';
import {
  Card, Button, Space, Tag, Modal, Input, Select, Message,
  Typography, Grid, Empty, Spin, Table, Popconfirm, Statistic, Divider,
} from '@arco-design/web-react';
import {
  IconPlus, IconDelete, IconFilter, IconMessage,
  IconThunderbolt, IconTrophy, IconExclamationCircle,
} from '@arco-design/web-react/icon';
import { feedbackApi } from '../api';

const { Title, Text, Paragraph } = Typography;
const { Row, Col } = Grid;
const { TextArea } = Input;

interface FeedbackItem {
  id: number;
  title: string;
  source_type: string;
  content: string;
  user_segment: string;
  sentiment_score: number;
  themes: string[];
  impact_level: string;
  status: string;
  recommendations: string[];
  author: string;
  created_at: string;
  updated_at: string;
}

interface FeedbackSummary {
  total: number;
  by_source: Record<string, number>;
  by_status: Record<string, number>;
  by_segment: Record<string, number>;
  sentiment_distribution: Record<string, number>;
  top_themes: { theme: string; count: number }[];
}

const sourceLabels: Record<string, string> = {
  bid: '📋 标书/投标',
  review: '⭐ 用户评价',
  ticket: '🎫 工单',
  interview: '🎤 访谈',
  survey: '📊 问卷',
  general: '📝 通用',
};

const segmentLabels: Record<string, string> = {
  enterprise: '🏢 企业客户',
  core: '💎 核心用户',
  new: '🌱 新用户',
  churned: '👋 流失用户',
  unknown: '❓ 未分类',
};

const impactColors: Record<string, string> = {
  critical: 'red',
  high: 'orange',
  medium: 'arcoblue',
  low: 'gray',
};

const statusLabels: Record<string, { label: string; color: string }> = {
  new: { label: '待分析', color: 'gray' },
  analyzing: { label: '分析中', color: 'orange' },
  analyzed: { label: '已分析', color: 'arcoblue' },
  actioned: { label: '已执行', color: 'green' },
  archived: { label: '已归档', color: 'purple' },
};

const sentimentEmoji = (score: number): string => {
  if (score <= -2) return '😡';
  if (score === -1) return '😟';
  if (score === 0) return '😐';
  if (score === 1) return '🙂';
  return '😊';
};

const FeedbackAnalysis: React.FC = () => {
  const [feedbackList, setFeedbackList] = useState<FeedbackItem[]>([]);
  const [summary, setSummary] = useState<FeedbackSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [filterSource, setFilterSource] = useState('');
  const [filterStatus, setFilterStatus] = useState('');
  const [detailVisible, setDetailVisible] = useState(false);
  const [selectedItem, setSelectedItem] = useState<FeedbackItem | null>(null);
  const [addVisible, setAddVisible] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newContent, setNewContent] = useState('');
  const [newSource, setNewSource] = useState('general');
  const [newSegment, setNewSegment] = useState('unknown');
  const [newAuthor, setNewAuthor] = useState('');
  const [newSentiment, setNewSentiment] = useState(0);
  const [newImpact, setNewImpact] = useState('medium');

  const fetchData = async () => {
    setLoading(true);
    const [listRes, summaryRes] = await Promise.all([
      feedbackApi.list(filterSource, filterStatus).catch(console.error),
      feedbackApi.summary().catch(console.error),
    ]);
    if (listRes?.data) setFeedbackList(listRes.data.feedback || []);
    if (summaryRes?.data) setSummary(summaryRes.data);
    setLoading(false);
  };

  useEffect(() => { fetchData(); }, [filterSource, filterStatus]);

  const handleAdd = async () => {
    if (!newTitle.trim() || !newContent.trim() || !newAuthor.trim()) {
      Message.error('请填写标题、内容和负责人');
      return;
    }
    await feedbackApi.create({
      title: newTitle,
      content: newContent,
      source_type: newSource,
      user_segment: newSegment,
      author: newAuthor,
      sentiment_score: newSentiment,
      impact_level: newImpact,
    }).catch(console.error);
    Message.success('反馈已添加');
    setAddVisible(false);
    setNewTitle(''); setNewContent(''); setNewAuthor('');
    fetchData();
  };

  const handleDelete = async (id: number) => {
    await feedbackApi.delete(id).catch(console.error);
    Message.success('反馈已删除');
    fetchData();
  };

  const handleStatusChange = async (id: number, status: string) => {
    await feedbackApi.update(id, { status }).catch(console.error);
    Message.success('状态已更新');
    fetchData();
  };

  const columns = [
    {
      title: '标题',
      dataIndex: 'title',
      width: 240,
      render: (val: string, record: FeedbackItem) => (
        <div className="cursor-pointer hover:text-[#165DFF]" onClick={() => { setSelectedItem(record); setDetailVisible(true); }}>
          <Text className="font-medium">{val}</Text>
        </div>
      ),
    },
    {
      title: '来源',
      dataIndex: 'source_type',
      width: 110,
      render: (val: string) => <span className="text-sm">{sourceLabels[val] || val}</span>,
    },
    {
      title: '用户群',
      dataIndex: 'user_segment',
      width: 100,
      render: (val: string) => <span className="text-sm">{segmentLabels[val] || val}</span>,
    },
    {
      title: '情绪',
      dataIndex: 'sentiment_score',
      width: 60,
      render: (val: number) => <span className="text-lg">{sentimentEmoji(val)}</span>,
    },
    {
      title: '影响',
      dataIndex: 'impact_level',
      width: 80,
      render: (val: string) => <Tag color={impactColors[val]} size="small">{val.toUpperCase()}</Tag>,
    },
    {
      title: '状态',
      dataIndex: 'status',
      width: 100,
      render: (val: string, record: FeedbackItem) => (
        <Select
          size="small"
          value={val}
          onChange={(v) => handleStatusChange(record.id, v)}
          style={{ width: 90 }}
          triggerProps={{ autoAlignPopupWidth: false }}
        >
          {Object.entries(statusLabels).map(([k, v]) => (
            <Select.Option key={k} value={k}>{v.label}</Select.Option>
          ))}
        </Select>
      ),
    },
    {
      title: '主题',
      dataIndex: 'themes',
      width: 200,
      render: (themes: string[]) => (
        <Space size={4} wrap>
          {(themes || []).slice(0, 3).map((t) => (
            <Tag key={t} size="small" bordered>{t}</Tag>
          ))}
          {themes && themes.length > 3 && <Text type="secondary" className="text-xs">+{themes.length - 3}</Text>}
        </Space>
      ),
    },
    {
      title: '负责人',
      dataIndex: 'author',
      width: 80,
    },
    {
      title: '操作',
      width: 60,
      render: (_: unknown, record: FeedbackItem) => (
        <Popconfirm title="确定删除？" onOk={() => handleDelete(record.id)}>
          <Button type="text" status="danger" icon={<IconDelete />} size="small" />
        </Popconfirm>
      ),
    },
  ];

  return (
    <div>
      {/* Page Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <Title heading={4} style={{ margin: 0 }}>反馈分析中心</Title>
          <Text type="secondary" className="text-sm">收集标书、用户评价、访谈等反馈，智能分析并驱动产品迭代</Text>
        </div>
        <Space>
          <Button type="primary" icon={<IconPlus />} onClick={() => setAddVisible(true)}>添加反馈</Button>
        </Space>
      </div>

      {/* Summary Cards */}
      {summary && (
        <Row gutter={16} className="mb-6">
          <Col span={4}>
            <Card style={{ borderRadius: 12 }}>
              <Statistic title="反馈总数" value={summary.total} suffix="条" />
            </Card>
          </Col>
          <Col span={5}>
            <Card style={{ borderRadius: 12 }}>
              <div className="text-xs text-[#86909C] mb-1">情绪分布</div>
              <div className="flex items-center gap-2 text-sm">
                <span>😡{summary.sentiment_distribution?.["-2"] || 0}</span>
                <span>😟{summary.sentiment_distribution?.["-1"] || 0}</span>
                <span>😐{summary.sentiment_distribution?.["0"] || 0}</span>
                <span>🙂{summary.sentiment_distribution?.["1"] || 0}</span>
                <span>😊{summary.sentiment_distribution?.["2"] || 0}</span>
              </div>
            </Card>
          </Col>
          <Col span={5}>
            <Card style={{ borderRadius: 12 }}>
              <div className="text-xs text-[#86909C] mb-1">来源分布</div>
              <Space size={4} wrap>
                {Object.entries(summary.by_source || {}).map(([k, v]) => (
                  <Tag key={k} size="small">{sourceLabels[k]?.split(' ')[0] || k} {v}</Tag>
                ))}
              </Space>
            </Card>
          </Col>
          <Col span={10}>
            <Card style={{ borderRadius: 12 }}>
              <div className="text-xs text-[#86909C] mb-1">热门主题 TOP 5</div>
              <Space size={4} wrap>
                {(summary.top_themes || []).slice(0, 5).map(({ theme, count }) => (
                  <Tag key={theme} color="arcoblue" size="small">
                    {theme} <span className="text-xs opacity-70">×{count}</span>
                  </Tag>
                ))}
                {(!summary.top_themes || summary.top_themes.length === 0) && (
                  <Text type="secondary" className="text-xs">暂无主题数据</Text>
                )}
              </Space>
            </Card>
          </Col>
        </Row>
      )}

      {/* Filters + Table */}
      <Card style={{ borderRadius: 12 }}>
        <div className="flex items-center gap-3 mb-4">
          <Select
            placeholder="来源筛选"
            allowClear
            value={filterSource || undefined}
            onChange={(val) => setFilterSource(val || '')}
            style={{ width: 140 }}
          >
            {Object.entries(sourceLabels).map(([k, v]) => (
              <Select.Option key={k} value={k}>{v}</Select.Option>
            ))}
          </Select>
          <Select
            placeholder="状态筛选"
            allowClear
            value={filterStatus || undefined}
            onChange={(val) => setFilterStatus(val || '')}
            style={{ width: 120 }}
          >
            {Object.entries(statusLabels).map(([k, v]) => (
              <Select.Option key={k} value={k}>{v.label}</Select.Option>
            ))}
          </Select>
        </div>
        <Table
          columns={columns}
          data={feedbackList}
          loading={loading}
          rowKey="id"
          pagination={{ pageSize: 10, showTotal: true }}
          noDataElement={<Empty description="暂无反馈数据。在 CodeBuddy 中使用 feedback-insight-engine skill 收集反馈。" />}
        />
      </Card>

      {/* Detail Modal */}
      <Modal
        title="反馈详情"
        visible={detailVisible}
        onCancel={() => setDetailVisible(false)}
        style={{ width: 700 }}
        footer={<Button onClick={() => setDetailVisible(false)}>关闭</Button>}
      >
        {selectedItem && (
          <div>
            <Title heading={5} style={{ margin: '0 0 12px 0' }}>{selectedItem.title}</Title>
            <Space className="mb-4" wrap>
              <Tag>{sourceLabels[selectedItem.source_type]}</Tag>
              <Tag>{segmentLabels[selectedItem.user_segment]}</Tag>
              <Tag color={impactColors[selectedItem.impact_level]}>{selectedItem.impact_level.toUpperCase()}</Tag>
              <span className="text-lg">{sentimentEmoji(selectedItem.sentiment_score)}</span>
              <Text type="secondary">by {selectedItem.author}</Text>
            </Space>

            <Divider className="my-3" />

            <div className="mb-4">
              <Text className="font-medium block mb-2">原始反馈内容</Text>
              <div className="p-3 rounded-lg whitespace-pre-wrap text-sm leading-relaxed"
                style={{ background: '#F7F8FA' }}>
                {selectedItem.content}
              </div>
            </div>

            {selectedItem.themes.length > 0 && (
              <div className="mb-4">
                <Text className="font-medium block mb-2">主题标签</Text>
                <Space wrap>
                  {selectedItem.themes.map((t) => (
                    <Tag key={t} color="arcoblue">{t}</Tag>
                  ))}
                </Space>
              </div>
            )}

            {selectedItem.recommendations.length > 0 && (
              <div className="mb-4">
                <Text className="font-medium block mb-2">迭代建议</Text>
                <div className="space-y-2">
                  {selectedItem.recommendations.map((r, i) => (
                    <div key={i} className="flex items-start gap-2 p-2 rounded-lg"
                      style={{ background: '#E8FFEA' }}>
                      <IconThunderbolt style={{ color: '#00B42A', flexShrink: 0, marginTop: 2 }} />
                      <Text className="text-sm">{r}</Text>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </Modal>

      {/* Add Feedback Modal */}
      <Modal
        title="添加反馈"
        visible={addVisible}
        onCancel={() => setAddVisible(false)}
        onOk={handleAdd}
        style={{ width: 600 }}
      >
        <Space direction="vertical" className="w-full" size={12}>
          <Input
            placeholder="反馈标题（如：XX企业投标反馈 — 数据导出不足）"
            value={newTitle}
            onChange={setNewTitle}
          />
          <div className="flex gap-3">
            <Select value={newSource} onChange={setNewSource} style={{ flex: 1 }}>
              {Object.entries(sourceLabels).map(([k, v]) => (
                <Select.Option key={k} value={k}>{v}</Select.Option>
              ))}
            </Select>
            <Select value={newSegment} onChange={setNewSegment} style={{ flex: 1 }}>
              {Object.entries(segmentLabels).map(([k, v]) => (
                <Select.Option key={k} value={k}>{v}</Select.Option>
              ))}
            </Select>
          </div>
          <div className="flex gap-3">
            <Select value={newImpact} onChange={setNewImpact} style={{ flex: 1 }}>
              <Select.Option value="critical">🔴 Critical</Select.Option>
              <Select.Option value="high">🟠 High</Select.Option>
              <Select.Option value="medium">🔵 Medium</Select.Option>
              <Select.Option value="low">⚪ Low</Select.Option>
            </Select>
            <Select value={String(newSentiment)} onChange={(v) => setNewSentiment(Number(v))} style={{ flex: 1 }}>
              <Select.Option value="-2">😡 非常不满</Select.Option>
              <Select.Option value="-1">😟 不满</Select.Option>
              <Select.Option value="0">😐 中性</Select.Option>
              <Select.Option value="1">🙂 满意</Select.Option>
              <Select.Option value="2">😊 非常满意</Select.Option>
            </Select>
          </div>
          <Input placeholder="负责人姓名" value={newAuthor} onChange={setNewAuthor} />
          <TextArea
            placeholder="粘贴原始反馈内容（标书评审意见、用户评价、访谈记录等）"
            value={newContent}
            onChange={setNewContent}
            autoSize={{ minRows: 6, maxRows: 15 }}
          />
        </Space>
      </Modal>
    </div>
  );
};

export default FeedbackAnalysis;
