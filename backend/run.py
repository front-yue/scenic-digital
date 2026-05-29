import sys
import os

# 获取实际运行目录（支持 PyInstaller 打包）
if getattr(sys, 'frozen', False):
    # 打包后的路径
    BASE_DIR = sys._MEIPASS
    RUNTIME_DIR = os.path.dirname(sys.executable)
else:
    # 开发环境路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    RUNTIME_DIR = BASE_DIR

# 将目录加入到 Python 模块搜索路径
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 智慧文旅数字人体验平台 - 后端服务")
    print("=" * 60)
    print(f"📁 运行目录: {RUNTIME_DIR}")
    print(f"🌐 服务地址: http://0.0.0.0:8888")
    print("=" * 60)
    
    # 生产环境建议将 debug 改为 False
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=8888, debug=debug_mode)