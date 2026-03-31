#!/bin/bash
# ──────────────────────────────────────────────────
# PM Team Hub — 团队部署启动脚本
# 
# 用法:
#   ./scripts/start-server.sh              # 本地开发模式
#   ./scripts/start-server.sh --team       # 团队共享模式（打印团队配置指引）
#
# 前提:
#   1. Python 3.9+
#   2. cd mcp-server && pip install -r requirements.txt
# ──────────────────────────────────────────────────

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MCP_DIR="$PROJECT_ROOT/mcp-server"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get local IP for team mode
get_local_ip() {
    if command -v ipconfig &> /dev/null; then
        # macOS
        ipconfig getifaddr en0 2>/dev/null || echo "127.0.0.1"
    elif command -v hostname &> /dev/null; then
        # Linux
        hostname -I 2>/dev/null | awk '{print $1}' || echo "127.0.0.1"
    else
        echo "127.0.0.1"
    fi
}

echo -e "${GREEN}🚀 PM Team Hub — 启动服务${NC}"
echo ""

# Check team mode
if [ "$1" = "--team" ]; then
    LOCAL_IP=$(get_local_ip)
    PORT=${PORT:-8000}
    
    echo -e "${BLUE}══════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  📡 团队共享模式${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  服务地址:  ${GREEN}http://$LOCAL_IP:$PORT${NC}"
    echo -e "  API 文档:  ${GREEN}http://$LOCAL_IP:$PORT/docs${NC}"
    echo -e "  MCP 端点:  ${GREEN}http://$LOCAL_IP:$PORT/mcp/sse${NC}"
    echo ""
    echo -e "${YELLOW}  📋 团队成员配置步骤:${NC}"
    echo ""
    echo "  1. 在项目根目录创建 .mcp.json:"
    echo ""
    echo "     {"
    echo "       \"mcpServers\": {"
    echo "         \"pm-team-hub\": {"
    echo "           \"type\": \"sse\","
    echo "           \"url\": \"http://$LOCAL_IP:$PORT/mcp/sse\""
    echo "         }"
    echo "       }"
    echo "     }"
    echo ""
    echo "  2. 前端连接后端（开发模式）:"
    echo ""
    echo "     VITE_API_URL=http://$LOCAL_IP:$PORT npm run dev"
    echo ""
    echo -e "${BLUE}══════════════════════════════════════════════════${NC}"
    echo ""
fi

# Start backend
cd "$MCP_DIR"

echo -e "${GREEN}📦 启动后端服务...${NC}"
echo "   目录: $MCP_DIR"
echo ""

# Create data directory
mkdir -p data

# Run server
python main.py
