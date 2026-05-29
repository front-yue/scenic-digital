import os
import sys
from dotenv import load_dotenv

# 获取 .env 文件路径
if getattr(sys, 'frozen', False):
    # PyInstaller 打包后：从 exe 同级目录加载
    BASE_DIR = os.path.dirname(sys.executable)
    env_path = os.path.join(BASE_DIR, '.env')
else:
    # 开发环境：从项目目录加载
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(BASE_DIR, '.env')

# 加载 .env 文件
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    # 尝试默认加载
    load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'

    # 图片上传配置
    if getattr(sys, 'frozen', False):
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    else:
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # 数据库配置
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')

    # 高德地图配置
    AMAP_KEY = os.getenv('AMAP_KEY', '')
