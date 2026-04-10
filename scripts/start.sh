#!/bin/bash

# 设置输出颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}===================================================${NC}"
echo -e "${GREEN}      智慧文旅数字大屏 - 一键启动脚本${NC}"
echo -e "${GREEN}===================================================${NC}"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}[错误] 未检测到 python3，请确保已安装 Python3。${NC}"
    exit 1
fi

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null
then
    echo -e "${RED}[错误] 未检测到 node，请确保已安装 Node.js。${NC}"
    exit 1
fi

# 获取脚本所在目录的绝对路径，并切换到项目根目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.." || exit 1

# 启动后端服务
echo -e "${YELLOW}[1/2] 正在启动 Flask 后端服务...${NC}"
cd backend || exit 1

if [ ! -d "venv" ]; then
    echo -e "  - 检测到尚未创建虚拟环境，正在创建..."
    python3 -m venv venv
    echo -e "  - 正在安装后端依赖..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 后台运行后端服务
echo -e "  - 正在运行后端服务..."
python run.py &
BACKEND_PID=$!
cd ..
echo -e "${GREEN}[成功] 后端服务已在后台启动！(PID: $BACKEND_PID)${NC}"
echo ""

# 启动前端服务
echo -e "${YELLOW}[2/2] 正在启动 Vue 前端服务...${NC}"
if [ ! -d "node_modules" ]; then
    echo -e "  - 检测到尚未安装前端依赖，正在安装..."
    npm install
fi

echo -e "  - 正在启动前端开发服务器..."
npm run dev

# 退出时清理后台进程
trap 'echo -e "${YELLOW}正在关闭服务...${NC}"; kill $BACKEND_PID; exit' SIGINT SIGTERM
