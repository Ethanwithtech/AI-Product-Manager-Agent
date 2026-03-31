import React, { useState, useEffect } from 'react';
import {
  Card, Button, Space, Tag, Modal, Input, Select, Message,
  Typography, Grid, Empty, Spin, Descriptions,
} from '@arco-design/web-react';
import { IconPlus, IconEdit, IconDelete, IconFilter } from '@arco-design/web-react/icon';
import ReactMarkdown from 'react-markdown';
import { requirementsApi } from '../api';

const { Title, Text, Paragraph } = Typography;
const { Row, Col } = Grid;
const { TextArea } = Input;

interface Requirement {
  id: number;
  title: string;
  content: string;
  status: string;
  modules: string[];
  keywords: string[];
  author: string;
  created_at: string;
  updated_at: string;
}

const statusColors: Record<string, string> = {
  draft: 'gray',
  review: 'orange',
  approved: 'green',
  archived: 'purple',
};

const statusLabels: Record<string, string> = {
  draft: '草稿',
  review: '评审中',
  approved: '已通过',
  archived: '已归档',
};

const Requirements: React.FC = () => {
  const [requirements, setRequirements] = useState<Requirement[]>([]);
  const [loading, setLoading] = useState(false);
  const [filterStatus, setFilterStatus] = useState('');
  const [detailVisible, setDetailVisible] = useState(false);
  const [selectedReq, setSelectedReq] = useState<Requirement | null>(null);
  const [editing, setEditing] = useState(false);
  const [editContent, setEditContent] = useState('');
  const [editTitle, setEditTitle] = useState('');

  const fetchRequirements = async () => {
    setLoading(true);
    const res = await requirementsApi.list(filterStatus).catch(console.error);
    if (res?.data) setRequirements(res.data.requirements || []);
    setLoading(false);
  };

  useEffect(() => { fetchRequirements(); }, [filterStatus]);

  const handleOpenDetail = (req: Requirement) => {
    setSelectedReq(req);
    setEditTitle(req.title);
    setEditContent(req.content);
    setDetailVisible(true);
    setEditing(false);
  };

  const handleSave = async () => {
    if (!selectedReq) return;
    await requirementsApi.update(selectedReq.id, {
      title: editTitle,
      content: editContent,
    }).catch(console.error);
    Message.success('需求单已更新');
    setEditing(false);
    fetchRequirements();
  };

  const handleStatusChange = async (id: number, status: string) => {
    await requirementsApi.update(id, { status }).catch(console.error);
    Message.success('状态已更新');
    fetchRequirements();
  };

  const handleDelete = async (id: number) => {
    await requirementsApi.delete(id).catch(console.error);
    Message.success('需求单已删除');
    fetchRequirements();
  };

  return (
    <div>
      {/* Page Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <Title heading={4} style={{ margin: 0 }}>需求单管理</Title>
          <Text type="secondary" className="text-sm">查看和编辑通过 AI 生成的需求文档</Text>
        </div>
        <Space>
          <Select
            placeholder="筛选状态"
            allowClear
            value={filterStatus || undefined}
            onChange={(val) => setFilterStatus(val || '')}
            style={{ width: 140 }}
            prefix={<IconFilter />}
          >
            <Select.Option value="draft">草稿</Select.Option>
            <Select.Option value="review">评审中</Select.Option>
            <Select.Option value="approved">已通过</Select.Option>
            <Select.Option value="archived">已归档</Select.Option>
          </Select>
        </Space>
      </div>

      {/* Requirements Grid */}
      {loading ? (
        <div className="flex justify-center py-20"><Spin size={32} /></div>
      ) : requirements.length === 0 ? (
        <Card style={{ borderRadius: 12 }}>
          <Empty description="暂无需求单。在 CodeBuddy 中使用 /generate-requirement 命令生成。" />
        </Card>
      ) : (
        <Row gutter={[16, 16]}>
          {requirements.map((req) => (
            <Col key={req.id} span={8}>
              <Card
                hoverable
                className="cursor-pointer group"
                style={{ borderRadius: 12, height: '100%' }}
                onClick={() => handleOpenDetail(req)}
              >
                <div className="flex items-start justify-between mb-3">
                  <Title heading={6} style={{ margin: 0, flex: 1 }} ellipsis={{ rows: 1 }}>
                    {req.title}
                  </Title>
                  <Tag color={statusColors[req.status]} size="small" className="ml-2 flex-shrink-0">
                    {statusLabels[req.status] || req.status}
                  </Tag>
                </div>
                <Paragraph type="secondary" ellipsis={{ rows: 2 }} className="text-sm mb-3">
                  {req.content.replace(/[#*`>\[\]()-]/g, ' ').slice(0, 150)}
                </Paragraph>
                <div className="flex items-center justify-between">
                  <Space size={4} wrap>
                    {(req.modules || []).slice(0, 3).map((m) => (
                      <Tag key={m} size="small" color="arcoblue" bordered>{m}</Tag>
                    ))}
                  </Space>
                  <Text type="secondary" className="text-xs">{req.author}</Text>
                </div>
                <Text type="secondary" className="text-xs block mt-2">
                  {req.updated_at ? new Date(req.updated_at).toLocaleString('zh-CN') : ''}
                </Text>
              </Card>
            </Col>
          ))}
        </Row>
      )}

      {/* Detail Modal */}
      <Modal
        title={editing ? '编辑需求单' : '需求单详情'}
        visible={detailVisible}
        onCancel={() => setDetailVisible(false)}
        style={{ width: 900 }}
        footer={
          editing ? (
            <Space>
              <Button onClick={() => setEditing(false)}>取消</Button>
              <Button type="primary" onClick={handleSave}>保存</Button>
            </Space>
          ) : (
            <Space>
              <Select
                value={selectedReq?.status}
                onChange={(val) => selectedReq && handleStatusChange(selectedReq.id, val)}
                style={{ width: 120 }}
              >
                <Select.Option value="draft">草稿</Select.Option>
                <Select.Option value="review">评审中</Select.Option>
                <Select.Option value="approved">已通过</Select.Option>
                <Select.Option value="archived">已归档</Select.Option>
              </Select>
              <Button icon={<IconEdit />} onClick={() => setEditing(true)}>编辑</Button>
              <Button
                status="danger"
                icon={<IconDelete />}
                onClick={() => {
                  if (selectedReq) { handleDelete(selectedReq.id); setDetailVisible(false); }
                }}
              >删除</Button>
            </Space>
          )
        }
      >
        {selectedReq && (
          <div>
            {editing ? (
              <Space direction="vertical" className="w-full" size={12}>
                <Input
                  value={editTitle}
                  onChange={setEditTitle}
                  placeholder="需求单标题"
                  size="large"
                />
                <TextArea
                  value={editContent}
                  onChange={setEditContent}
                  autoSize={{ minRows: 15, maxRows: 30 }}
                  placeholder="Markdown 格式的需求单内容"
                  style={{ fontFamily: 'monospace', fontSize: 13 }}
                />
              </Space>
            ) : (
              <div>
                <Descriptions
                  data={[
                    { label: '作者', value: selectedReq.author },
                    { label: '状态', value: <Tag color={statusColors[selectedReq.status]}>{statusLabels[selectedReq.status]}</Tag> },
                    { label: '模块', value: (selectedReq.modules || []).map(m => <Tag key={m} size="small">{m}</Tag>) },
                    { label: '更新时间', value: selectedReq.updated_at ? new Date(selectedReq.updated_at).toLocaleString('zh-CN') : '-' },
                  ]}
                  className="mb-4"
                  column={2}
                />
                <div className="markdown-content border rounded-lg p-4"
                  style={{ background: '#FAFBFC', maxHeight: 500, overflowY: 'auto' }}>
                  <ReactMarkdown>{selectedReq.content}</ReactMarkdown>
                </div>
              </div>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Requirements;
