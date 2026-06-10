from flask import Flask, send_from_directory, request
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

    # 管理后台密码验证接口
    @app.route('/api/admin/verify', methods=['POST'])
    def verify_admin():
        data = request.get_json() or {}
        password = data.get('password', '')
        if password == app.config.get('ADMIN_PASSWORD'):
            return ApiResponse.success(message="验证通过")
        return ApiResponse.error(message="密码错误", code=401)

    # 注册蓝图 (路由)
    from app.routes.scenic_info_routes import scenic_info_bp
    from app.routes.spot_routes import spot_bp
    from app.routes.upload_routes import upload_bp
    from app.routes.map_routes import map_bp
    from app.routes.config_routes import config_bp

    app.register_blueprint(scenic_info_bp, url_prefix='/api/scenic')
    app.register_blueprint(spot_bp, url_prefix='/api/scenic')
    app.register_blueprint(config_bp, url_prefix='/api/config')
    
    app.register_blueprint(upload_bp, url_prefix='/api')
    
    app.register_blueprint(map_bp, url_prefix='/api/map')

    return app
