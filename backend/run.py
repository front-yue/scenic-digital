import sys
import os

# 将 backend 根目录加入到 Python 模块搜索路径中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("🚀 [Backend] Starting Flask server on http://127.0.0.1:8888")
    # debug=True 可以在代码修改时自动热重载
    app.run(host='0.0.0.0', port=8888, debug=True)