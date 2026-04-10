from flask import Blueprint

# 创建一个总的蓝图，用于管理 /api/scenic 下的所有路由
scenic_bp = Blueprint('scenic', __name__)

# 导入子路由，利用 Flask 的路由注册机制，直接将子路由挂载到总蓝图上
from . import scenic_info_routes
from . import spot_routes
from . import upload_routes