from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from app.utils.response import ApiResponse
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # 解决 Flask jsonify 返回中文时被转义为 Unicode 的问题
    app.json.ensure_ascii = False

    # 允许跨域请求，方便前端调试
    CORS(app)

    # 配置文件服务器路由，用于前端访问上传的图片
    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # 添加根路由测试接口
    @app.route('/')
    def index():
        return ApiResponse.success(message="智慧文旅后端服务已启动 🚀")

    # 注册蓝图 (路由)
    from app.routes import scenic_bp

    app.register_blueprint(scenic_bp, url_prefix='/api/scenic')

    return app
