@echo off
chcp 65001 >nul
color 0A

echo ===================================================
echo       智慧文旅数字大屏 - 一键启动脚本
echo ===================================================
echo.

:: 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请确保已安装 Python 并添加到了系统环境变量中。
    pause
    exit /b 1
)

:: 检查 Node.js 是否安装
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js，请确保已安装 Node.js 并添加到了系统环境变量中。
    pause
    exit /b 1
)

:: 切换到项目根目录 (即 scripts 的上一级)
cd /d "%~dp0.."

:: 启动后端服务
echo [1/2] 正在启动 Flask 后端服务...
cd backend
if not exist "venv" (
    echo   - 检测到尚未创建虚拟环境，正在创建...
    python -m venv venv
    echo   - 正在安装后端依赖...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

:: 开启一个新的命令窗口运行后端，防止阻塞
start "文旅大屏 - 后端服务 (端口 8888)" cmd /c "echo 正在运行后端服务... && call venv\Scripts\activate.bat && python run.py"

cd ..
echo [成功] 后端服务已在后台启动！
echo.

:: 启动前端服务
echo [2/2] 正在启动 Vue 前端服务...
if not exist "node_modules" (
    echo   - 检测到尚未安装前端依赖，正在安装...
    call npm install
)

:: 直接在当前窗口启动前端
echo   - 正在启动前端开发服务器...
call npm run dev

pause
