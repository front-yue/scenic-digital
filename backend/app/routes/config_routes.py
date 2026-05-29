from flask import Blueprint, request
from app.services.config_service import ConfigService
from app.utils.response import ApiResponse

config_bp = Blueprint('config', __name__)
config_service = ConfigService()

@config_bp.route('/', methods=['GET'])
def get_all_config():
    """获取所有系统配置"""
    try:
        data = config_service.get_all_config()
        return ApiResponse.success(data)
    except Exception as e:
        return ApiResponse.error(f"获取配置失败: {str(e)}")

@config_bp.route('/<key>', methods=['GET'])
def get_config(key):
    """获取单个系统配置"""
    try:
        value = config_service.get_config(key)
        return ApiResponse.success({"key": key, "value": value})
    except Exception as e:
        return ApiResponse.error(f"获取配置失败: {str(e)}")

@config_bp.route('/<key>', methods=['PUT'])
def update_config(key):
    """更新系统配置"""
    data = request.get_json()
    value = data.get('value')
    if value is None:
        return ApiResponse.error("缺少 value 参数")
        
    try:
        config_service.update_config(key, value)
        return ApiResponse.success(None, "配置更新成功")
    except Exception as e:
        return ApiResponse.error(f"更新配置失败: {str(e)}")
