import React from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout as ArcoLayout, Menu, Typography, Space, Badge } from '@arco-design/web-react';
import { IconBook, IconFile, IconDashboard, IconSettings, IconApps, IconMessage } from '@arco-design/web-react/icon';

const { Sider, Header, Content } = ArcoLayout;
const { Title } = Typography;

const menuItems = [
  { key: 'knowledge', icon: <IconBook />, label: '知识库' },
  { key: 'requirements', icon: <IconFile />, label: '需求单' },
  { key: 'progress', icon: <IconDashboard />, label: '进度看板' },
  { key: 'feedback', icon: <IconMessage />, label: '反馈分析' },
  { key: 'templates', icon: <IconSettings />, label: '规则模板' },
];

const Layout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const currentKey = location.pathname.split('/')[1] || 'knowledge';

  return (
    <ArcoLayout className="h-screen">
      {/* Top Header */}
      <Header className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 h-14"
        style={{ background: 'linear-gradient(135deg, #165DFF 0%, #0E42D2 100%)', borderBottom: 'none' }}>
        <Space align="center" size={12}>
          <IconApps style={{ fontSize: 22, color: '#fff' }} />
          <Title heading={5} style={{ margin: 0, color: '#fff', letterSpacing: '0.5px' }}>
            PM Team Hub
          </Title>
        </Space>
        <Space align="center" size={16}>
          <Badge count={0} dot>
            <span className="text-white/80 text-sm cursor-pointer hover:text-white transition-colors">
              通知
            </span>
          </Badge>
          <span className="text-white/80 text-sm">
            管理台 v1.0
          </span>
        </Space>
      </Header>

      <ArcoLayout className="pt-14">
        {/* Sidebar */}
        <Sider
          width={220}
          className="fixed left-0 top-14 bottom-0 z-40"
          style={{
            background: '#fff',
            borderRight: '1px solid #E5E6EB',
            boxShadow: '2px 0 8px rgba(0,0,0,0.04)',
          }}
        >
          <div className="py-4">
            <Menu
              selectedKeys={[currentKey]}
              onClickMenuItem={(key) => navigate(`/${key}`)}
              style={{ border: 'none' }}
            >
              {menuItems.map((item) => (
                <Menu.Item key={item.key}>
                  <Space size={8}>
                    {item.icon}
                    <span>{item.label}</span>
                  </Space>
                </Menu.Item>
              ))}
            </Menu>
          </div>
          <div className="absolute bottom-4 left-4 right-4 p-3 rounded-lg"
            style={{ background: 'linear-gradient(135deg, #F0F5FF 0%, #E8F3FF 100%)' }}>
            <p className="text-xs text-[#4E5969] mb-1 font-medium">MCP Server</p>
            <p className="text-xs text-[#86909C] mb-2">连接您的 CodeBuddy 以使用 AI Skills</p>
            <p className="text-xs text-[#165DFF] cursor-pointer hover:underline"
              onClick={() => {
                localStorage.removeItem('pm-team-hub-guide-shown');
                window.dispatchEvent(new Event('open-guide'));
                window.location.reload();
              }}>
              💡 查看使用引导
            </p>
          </div>
        </Sider>

        {/* Main Content */}
        <Content className="ml-[220px] p-6 min-h-screen" style={{ background: '#F7F8FA' }}>
          <Outlet />
        </Content>
      </ArcoLayout>
    </ArcoLayout>
  );
};

export default Layout;
