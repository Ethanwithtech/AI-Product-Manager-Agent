import React, { useState, useEffect } from 'react';
import {
  Card, Table, Button, Upload, Space, Tag, Popconfirm, Message,
  Typography, Statistic, Grid, Input, Drawer, List, Spin, Empty,
} from '@arco-design/web-react';
import { IconUpload, IconSearch, IconDelete } from '@arco-design/web-react/icon';
import { knowledgeApi } from '../api';

const { Title, Text } = Typography;
const { Row, Col } = Grid;

interface KnowledgeDoc {
  id: number;
  title: string;
  doc_type: string;
  chunks: number;
  content_preview: string;
  created_at: string;
}

interface SearchResult {
  id: string;
  content: string;
  metadata: { doc_title: string; chunk_index: number };
  distance: number;
}

const KnowledgeBase: React.FC = () => {
  const [documents, setDocuments] = useState<KnowledgeDoc[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);
  const [totalChunks, setTotalChunks] = useState(0);

  const fetchDocuments = async () => {
    setLoading(true);
    const res = await knowledgeApi.list().catch((e) => { console.error(e); return null; });
    if (res?.data) {
      setDocuments(res.data.documents || []);
      setTotalChunks(res.data.stats?.total_chunks || 0);
    }
    setLoading(false);
  };

  useEffect(() => { fetchDocuments(); }, []);

  const handleDelete = async (id: number) => {
    await knowledgeApi.delete(id).catch(console.error);
    Message.success('文档已删除');
    fetchDocuments();
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setSearching(true);
    const res = await knowledgeApi.search(searchQuery).catch(console.error);
    if (res?.data) setSearchResults(res.data.results || []);
    setSearching(false);
  };

  const columns = [
    { title: '文档名称', dataIndex: 'title', sorter: (a: KnowledgeDoc, b: KnowledgeDoc) => a.title.localeCompare(b.title) },
    {
      title: '类型',
      dataIndex: 'doc_type',
      width: 80,
      render: (type: string) => {
        const colorMap: Record<string, string> = {
          pdf: 'red', md: 'arcoblue', txt: 'green', docx: 'purple', html: 'orangered',
        };
        return (
          <Tag color={colorMap[type] || 'gray'} size="small">
            {type.toUpperCase()}
          </Tag>
        );
      },
    },
    { title: '分块数', dataIndex: 'chunks', width: 80, sorter: (a: KnowledgeDoc, b: KnowledgeDoc) => a.chunks - b.chunks },
    {
      title: '上传时间', dataIndex: 'created_at', width: 180,
      render: (val: string) => val ? new Date(val).toLocaleString('zh-CN') : '-',
    },
    {
      title: '操作', width: 100,
      render: (_: unknown, record: KnowledgeDoc) => (
        <Popconfirm title="确定删除此文档？所有分块将被移除。" onOk={() => handleDelete(record.id)}>
          <Button type="text" status="danger" icon={<IconDelete />} size="small">删除</Button>
        </Popconfirm>
      ),
    },
  ];

  return (
    <div>
      {/* Page Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <Title heading={4} style={{ margin: 0 }}>产品知识库</Title>
          <Text type="secondary" className="text-sm">上传产品文档，为 AI Skills 提供产品上下文</Text>
        </div>
        <Button type="outline" icon={<IconSearch />} onClick={() => setSearchOpen(true)}>
          检索测试
        </Button>
      </div>

      {/* Statistics */}
      <Row gutter={16} className="mb-6">
        <Col span={8}>
          <Card className="hover:shadow-md transition-shadow" style={{ borderRadius: 12 }}>
            <Statistic title="文档总数" value={documents.length} suffix="篇" />
          </Card>
        </Col>
        <Col span={8}>
          <Card className="hover:shadow-md transition-shadow" style={{ borderRadius: 12 }}>
            <Statistic title="总分块数" value={totalChunks} suffix="块" />
          </Card>
        </Col>
        <Col span={8}>
          <Card className="hover:shadow-md transition-shadow" style={{ borderRadius: 12 }}>
            <Statistic
              title="知识库状态"
              value={documents.length > 0 ? '已就绪' : '待上传'}
              style={{ color: documents.length > 0 ? '#00B42A' : '#FF7D00' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Upload Area */}
      <Card className="mb-6" style={{ borderRadius: 12 }}>
        <Upload
          drag
          multiple
          accept=".md,.txt,.pdf,.docx,.html,.htm"
          tip="支持 Markdown (.md)、纯文本 (.txt)、PDF (.pdf)、Word (.docx)、HTML (.html) 格式"
          action="/api/knowledge"
          name="file"
          data={(file) => {
            const name = file?.name || '';
            const ext = name.split('.').pop()?.toLowerCase() || 'txt';
            const typeMap: Record<string, string> = {
              md: 'md', markdown: 'md', txt: 'txt', text: 'txt',
              pdf: 'pdf', docx: 'docx', doc: 'docx', html: 'html', htm: 'html',
            };
            return { doc_type: typeMap[ext] || 'txt', title: name || 'Untitled' };
          }}
          onChange={(_, currentFile) => {
            if (currentFile.status === 'done') {
              Message.success(`${currentFile.name} 上传成功`);
              fetchDocuments();
            } else if (currentFile.status === 'error') {
              Message.error(`${currentFile.name} 上传失败`);
            }
          }}
        />
      </Card>

      {/* Document List */}
      <Card title="文档列表" style={{ borderRadius: 12 }}>
        <Table
          columns={columns}
          data={documents}
          loading={loading}
          rowKey="id"
          pagination={{ pageSize: 10, showTotal: true }}
          noDataElement={<Empty description="暂无文档，上传产品文档以启用 AI 知识检索" />}
        />
      </Card>

      {/* Search Drawer */}
      <Drawer
        title="知识库检索测试"
        width={520}
        visible={searchOpen}
        onOk={() => setSearchOpen(false)}
        onCancel={() => setSearchOpen(false)}
        footer={null}
      >
        <Space direction="vertical" className="w-full" size={16}>
          <Input.Search
            placeholder="输入自然语言查询（如：我们的结账流程是怎样的？）"
            value={searchQuery}
            onChange={setSearchQuery}
            onSearch={handleSearch}
            loading={searching}
          />
          {searching && <Spin className="w-full flex justify-center" />}
          {!searching && searchResults.length > 0 && (
            <List
              dataSource={searchResults}
              render={(item: SearchResult, index: number) => (
                <List.Item key={item.id}>
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <Tag color="arcoblue" size="small">{item.metadata.doc_title}</Tag>
                      <Text type="secondary" className="text-xs">
                        相关度: {item.distance ? (1 - item.distance).toFixed(2) : 'N/A'}
                      </Text>
                    </div>
                    <Text className="text-sm leading-relaxed">
                      {item.content.slice(0, 300)}{item.content.length > 300 ? '...' : ''}
                    </Text>
                  </div>
                </List.Item>
              )}
            />
          )}
          {!searching && searchResults.length === 0 && searchQuery && (
            <Empty description="未找到相关文档" />
          )}
        </Space>
      </Drawer>
    </div>
  );
};

export default KnowledgeBase;
