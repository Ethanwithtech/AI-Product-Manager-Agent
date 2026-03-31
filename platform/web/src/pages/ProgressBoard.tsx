import React, { useState, useEffect } from 'react';
import {
  Card, Button, Space, Tag, Modal, Select, Message,
  Typography, Empty, Spin, Input,
} from '@arco-design/web-react';
import { IconPlus, IconExclamationCircle, IconRefresh } from '@arco-design/web-react/icon';
import { progressApi } from '../api';

const { Title, Text, Paragraph } = Typography;

interface ProgressItem {
  id: number;
  title: string;
  description: string;
  status: string;
  modules: string[];
  keywords: string[];
  author: string;
  updated_at: string;
}

interface Board {
  planning: ProgressItem[];
  in_progress: ProgressItem[];
  review: ProgressItem[];
  done: ProgressItem[];
}

const statusConfig: Record<string, { label: string; color: string; bg: string }> = {
  planning: { label: '📋 规划中', color: '#165DFF', bg: '#F0F5FF' },
  in_progress: { label: '🔨 进行中', color: '#FF7D00', bg: '#FFF7E8' },
  review: { label: '🔍 评审中', color: '#722ED1', bg: '#F5E8FF' },
  done: { label: '✅ 已完成', color: '#00B42A', bg: '#E8FFEA' },
};

const ProgressBoard: React.FC = () => {
  const [board, setBoard] = useState<Board>({ planning: [], in_progress: [], review: [], done: [] });
  const [loading, setLoading] = useState(false);
  const [filterAuthor, setFilterAuthor] = useState('');
  const [detailVisible, setDetailVisible] = useState(false);
  const [selectedItem, setSelectedItem] = useState<ProgressItem | null>(null);
  const [conflicts, setConflicts] = useState<any[]>([]);

  const fetchBoard = async () => {
    setLoading(true);
    const res = await progressApi.getBoard(filterAuthor).catch(console.error);
    if (res?.data) setBoard(res.data.board || { planning: [], in_progress: [], review: [], done: [] });
    setLoading(false);
  };

  useEffect(() => { fetchBoard(); }, [filterAuthor]);

  const handleCardClick = async (item: ProgressItem) => {
    setSelectedItem(item);
    setDetailVisible(true);
    // Check conflicts for this item
    const res = await progressApi.checkConflicts({
      title: item.title,
      modules: item.modules,
      keywords: item.keywords,
    }).catch(console.error);
    if (res?.data) setConflicts(res.data.conflicts || []);
  };

  const allAuthors = Array.from(new Set(
    [...board.planning, ...board.in_progress, ...board.review, ...board.done]
      .map(i => i.author)
  ));

  const renderColumn = (status: string, items: ProgressItem[]) => {
    const config = statusConfig[status];
    return (
      <div className="flex-1 min-w-[260px]" key={status}>
        <div className="flex items-center justify-between mb-3 px-2">
          <span className="font-medium text-sm" style={{ color: config.color }}>
            {config.label}
          </span>
          <Tag size="small" style={{ background: config.bg, color: config.color, border: 'none' }}>
            {items.length}
          </Tag>
        </div>
        <div className="space-y-3 min-h-[200px] p-2 rounded-xl" style={{ background: config.bg + '80' }}>
          {items.length === 0 ? (
            <div className="text-center py-8">
              <Text type="secondary" className="text-xs">暂无项目</Text>
            </div>
          ) : (
            items.map((item) => {
              const hasConflict = false; // Will be detected on click
              return (
                <Card
                  key={item.id}
                  hoverable
                  className="cursor-pointer group transition-all duration-200 hover:-translate-y-0.5"
                  style={{
                    borderRadius: 10,
                    borderLeft: hasConflict ? '3px solid #F53F3F' : '3px solid transparent',
                  }}
                  bodyStyle={{ padding: '12px 14px' }}
                  onClick={() => handleCardClick(item)}
                >
                  <div className="flex items-start justify-between mb-2">
                    <Text className="font-medium text-sm leading-tight flex-1" ellipsis>
                      {item.title}
                    </Text>
                    {hasConflict && (
                      <IconExclamationCircle className="text-danger flex-shrink-0 ml-1" />
                    )}
                  </div>
                  {item.description && (
                    <Paragraph type="secondary" ellipsis={{ rows: 2 }} className="text-xs mb-2" style={{ margin: 0 }}>
                      {item.description}
                    </Paragraph>
                  )}
                  <div className="flex items-center justify-between">
                    <Space size={4} wrap>
                      {(item.modules || []).slice(0, 2).map((m) => (
                        <Tag key={m} size="small" bordered className="text-xs">{m}</Tag>
                      ))}
                    </Space>
                    <div className="flex items-center gap-1">
                      <div className="w-5 h-5 rounded-full flex items-center justify-center text-xs text-white font-medium"
                        style={{ background: `hsl(${item.author.charCodeAt(0) * 37 % 360}, 60%, 55%)` }}>
                        {item.author.charAt(0).toUpperCase()}
                      </div>
                    </div>
                  </div>
                </Card>
              );
            })
          )}
        </div>
      </div>
    );
  };

  return (
    <div>
      {/* Page Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <Title heading={4} style={{ margin: 0 }}>产品进度看板</Title>
          <Text type="secondary" className="text-sm">查看所有 PM 的工作进度，检测功能冲突</Text>
        </div>
        <Space>
          <Select
            placeholder="筛选 PM"
            allowClear
            value={filterAuthor || undefined}
            onChange={(val) => setFilterAuthor(val || '')}
            style={{ width: 140 }}
          >
            {allAuthors.map((a) => (
              <Select.Option key={a} value={a}>{a}</Select.Option>
            ))}
          </Select>
          <Button icon={<IconRefresh />} onClick={fetchBoard}>刷新</Button>
        </Space>
      </div>

      {/* Kanban Board */}
      {loading ? (
        <div className="flex justify-center py-20"><Spin size={32} /></div>
      ) : (
        <div className="flex gap-4 overflow-x-auto pb-4">
          {renderColumn('planning', board.planning)}
          {renderColumn('in_progress', board.in_progress)}
          {renderColumn('review', board.review)}
          {renderColumn('done', board.done)}
        </div>
      )}

      {/* Detail Modal */}
      <Modal
        title="进度详情"
        visible={detailVisible}
        onCancel={() => { setDetailVisible(false); setConflicts([]); }}
        footer={<Button onClick={() => setDetailVisible(false)}>关闭</Button>}
        style={{ width: 600 }}
      >
        {selectedItem && (
          <div>
            <Title heading={5}>{selectedItem.title}</Title>
            <Space className="mb-3">
              <Tag color={statusConfig[selectedItem.status]?.color}>
                {statusConfig[selectedItem.status]?.label}
              </Tag>
              <Text type="secondary">负责人: {selectedItem.author}</Text>
            </Space>
            {selectedItem.description && (
              <Paragraph className="mb-3">{selectedItem.description}</Paragraph>
            )}
            <div className="mb-3">
              <Text className="font-medium text-sm mb-1 block">涉及模块</Text>
              <Space wrap>
                {(selectedItem.modules || []).map((m) => <Tag key={m}>{m}</Tag>)}
                {(!selectedItem.modules || selectedItem.modules.length === 0) && <Text type="secondary">无</Text>}
              </Space>
            </div>
            {conflicts.length > 0 && (
              <Card
                className="mt-4"
                style={{ borderColor: '#F53F3F', borderRadius: 8 }}
                title={<span className="text-danger">⚠️ 发现 {conflicts.length} 个潜在冲突</span>}
              >
                {conflicts.map((c, i) => (
                  <div key={i} className="mb-3 last:mb-0">
                    <Text className="font-medium">{c.type === 'module_overlap' ? '模块重叠' : '关键词重叠'}</Text>
                    <Paragraph type="secondary" className="text-sm mt-1">{c.recommendation}</Paragraph>
                  </div>
                ))}
              </Card>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
};

export default ProgressBoard;
