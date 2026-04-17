from flask import Blueprint

# 创建统一的 /api 蓝图
api_bp = Blueprint('api', __name__)

# 导入具体的路由模块并注册到统一个蓝图中
# 注意：导入必须在 Blueprint 实例化之后，否则会导致循环导入问题

from app.routes import scenic_bp
from app.routes.map_routes import map_bp

# 将之前分散的蓝图统统注册到这个主 api_bp 下
api_bp.register_blueprint(scenic_bp)
api_bp.register_blueprint(map_bp)