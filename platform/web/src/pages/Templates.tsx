import React, { useState, useEffect } from 'react';
import {
  Card, Button, Space, Tag, Input, Select, Message, Upload,
  Typography, List, Empty, Spin, Modal, Grid,
} from '@arco-design/web-react';
import { IconPlus, IconEdit, IconDelete, IconSave, IconUpload } from '@arco-design/web-react/icon';
import ReactMarkdown from 'react-markdown';
import { templatesApi } from '../api';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Row, Col } = Grid;

interface Template {
  id: number;
  name: string;
  category: string;
  content: string;
  created_at: string;
  updated_at: string;
}

const categoryConfig: Record<string, { label: string; color: string }> = {
  requirement: { label: '需求模板', color: 'arcoblue' },
  rule: { label: '团队规则', color: 'orange' },
  checklist: { label: '检查清单', color: 'green' },
};

const Templates: React.FC = () => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(false);
  const [filterCategory, setFilterCategory] = useState('all');
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [editing, setEditing] = useState(false);
  const [editName, setEditName] = useState('');
  const [editCategory, setEditCategory] = useState('requirement');
  const [editContent, setEditContent] = useState('');
  const [creating, setCreating] = useState(false);
  const [uploadCategory, setUploadCategory] = useState('requirement');

  const fetchTemplates = async () => {
    setLoading(true);
    const res = await templatesApi.list(filterCategory).catch(console.error);
    if (res?.data) setTemplates(res.data.templates || []);
    setLoading(false);
  };

  useEffect(() => { fetchTemplates(); }, [filterCategory]);

  const selectedTemplate = templates.find(t => t.id === selectedId);

  const handleSelect = (tpl: Template) => {
    setSelectedId(tpl.id);
    setEditName(tpl.name);
    setEditCategory(tpl.category);
    setEditContent(tpl.content);
    setEditing(false);
    setCreating(false);
  };

  const handleCreate = () => {
    setSelectedId(null);
    setEditName('');
    setEditCategory('requirement');
    setEditContent('');
    setEditing(true);
    setCreating(true);
  };

  const handleSave = async () => {
    if (!editName.trim() || !editContent.trim()) {
      Message.error('请填写模板名称和内容');
      return;
    }
    if (creating) {
      await templatesApi.create({ name: editName, category: editCategory, content: editContent }).catch(console.error);
      Message.success('模板已创建');
    } else if (selectedId) {
      await templatesApi.update(selectedId, { name: editName, category: editCategory, content: editContent }).catch(console.error);
      Message.success('模板已更新');
    }
    setEditing(false);
    setCreating(false);
    fetchTemplates();
  };

  const handleDelete = async (id: number) => {
    await templatesApi.delete(id).catch(console.error);
    Message.success('模板已删除');
    if (selectedId === id) { setSelectedId(null); setEditing(false); }
    fetchTemplates();
  };

  return (
    <div>
      {/* Page Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <Title heading={4} style={{ margin: 0 }}>规则与模板</Title>
          <Text type="secondary" className="text-sm">管理团队共享的需求模板、规则和检查清单</Text>
        </div>
        <Space>
          <Select
            value={filterCategory}
            onChange={setFilterCategory}
            style={{ width: 140 }}
          >
            <Select.Option value="all">全部</Select.Option>
            <Select.Option value="requirement">需求模板</Select.Option>
            <Select.Option value="rule">团队规则</Select.Option>
            <Select.Option value="checklist">检查清单</Select.Option>
          </Select>
          <Upload
            accept=".md,.txt,.docx,.pdf"
            showUploadList={false}
            action="/api/templates/upload"
            name="file"
            data={() => ({ category: uploadCategory })}
            onChange={(_, currentFile) => {
              if (currentFile.status === 'done') {
                Message.success(`模板文件 ${currentFile.name} 导入成功`);
                fetchTemplates();
              } else if (currentFile.status === 'error') {
                Message.error(`模板文件 ${currentFile.name} 导入失败`);
              }
            }}
          >
            <Button icon={<IconUpload />}>上传模板文件</Button>
          </Upload>
          <Select
            value={uploadCategory}
            onChange={setUploadCategory}
            style={{ width: 100 }}
            size="small"
          >
            <Select.Option value="requirement">需求模板</Select.Option>
            <Select.Option value="rule">团队规则</Select.Option>
            <Select.Option value="checklist">检查清单</Select.Option>
          </Select>
          <Button type="primary" icon={<IconPlus />} onClick={handleCreate}>新建模板</Button>
        </Space>
      </div>

      <Row gutter={16}>
        {/* Left Panel — Template List */}
        <Col span={8}>
          <Card style={{ borderRadius: 12, minHeight: 500 }} bodyStyle={{ padding: 0 }}>
            {loading ? (
              <div className="flex justify-center py-12"><Spin /></div>
            ) : templates.length === 0 ? (
              <Empty className="py-12" description="暂无模板，点击新建创建第一个模板" />
            ) : (
              <div className="divide-y divide-gray-100">
                {templates.map((tpl) => (
                  <div
                    key={tpl.id}
                    className={`px-4 py-3 cursor-pointer transition-colors hover:bg-blue-50 ${
                      selectedId === tpl.id ? 'bg-blue-50 border-l-2 border-primary' : ''
                    }`}
                    onClick={() => handleSelect(tpl)}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <Text className="font-medium text-sm" ellipsis>{tpl.name}</Text>
                      <Tag
                        size="small"
                        color={categoryConfig[tpl.category]?.color || 'gray'}
                      >
                        {categoryConfig[tpl.category]?.label || tpl.category}
                      </Tag>
                    </div>
                    <Text type="secondary" className="text-xs">
                      {tpl.updated_at ? new Date(tpl.updated_at).toLocaleString('zh-CN') : ''}
                    </Text>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </Col>

        {/* Right Panel — Editor/Preview */}
        <Col span={16}>
          <Card
            style={{ borderRadius: 12, minHeight: 500 }}
            title={
              editing ? (
                <Space>
                  <Input
                    value={editName}
                    onChange={setEditName}
                    placeholder="模板名称"
                    style={{ width: 200 }}
                  />
                  <Select value={editCategory} onChange={setEditCategory} style={{ width: 120 }}>
                    <Select.Option value="requirement">需求模板</Select.Option>
                    <Select.Option value="rule">团队规则</Select.Option>
                    <Select.Option value="checklist">检查清单</Select.Option>
                  </Select>
                </Space>
              ) : (
                selectedTemplate?.name || '选择一个模板查看'
              )
            }
            extra={
              editing ? (
                <Space>
                  <Button onClick={() => { setEditing(false); setCreating(false); }}>取消</Button>
                  <Button type="primary" icon={<IconSave />} onClick={handleSave}>保存</Button>
                </Space>
              ) : selectedTemplate ? (
                <Space>
                  <Button icon={<IconEdit />} onClick={() => setEditing(true)}>编辑</Button>
                  <Button
                    status="danger"
                    icon={<IconDelete />}
                    onClick={() => handleDelete(selectedTemplate.id)}
                  >删除</Button>
                </Space>
              ) : null
            }
          >
            {editing ? (
              <TextArea
                value={editContent}
                onChange={setEditContent}
                autoSize={{ minRows: 18, maxRows: 35 }}
                placeholder="使用 Markdown 格式编写模板内容..."
                style={{ fontFamily: 'monospace', fontSize: 13 }}
              />
            ) : selectedTemplate ? (
              <div className="markdown-content" style={{ maxHeight: 600, overflowY: 'auto' }}>
                <ReactMarkdown>{selectedTemplate.content}</ReactMarkdown>
              </div>
            ) : (
              <Empty description="从左侧列表选择一个模板，或点击新建创建" />
            )}
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Templates;
