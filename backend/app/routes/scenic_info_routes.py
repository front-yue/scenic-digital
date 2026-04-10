from flask import request
from app.services.scenic_info_service import ScenicInfoService
from app.utils.response import ApiResponse
from . import scenic_bp

scenic_info_service = ScenicInfoService()

@scenic_bp.route('/info', methods=['GET'])
def get_scenic_info():
    """获取景区全局信息接口"""
    try:
        data = scenic_info_service.get_info()
        return ApiResponse.success(data)
    except Exception as e:
        return ApiResponse.error(str(e))

@scenic_bp.route('/info', methods=['POST'])
def add_scenic_info():
    """新增景区概况"""
    data = request.get_json()
    try:
        new_id = scenic_info_service.add_info(data)
        return ApiResponse.success({"id": new_id}, "新增成功")
    except Exception as e:
        return ApiResponse.error(str(e))

@scenic_bp.route('/info/<int:info_id>', methods=['PUT'])
def update_scenic_info(info_id):
    """更新景区概况"""
    data = request.get_json()
    try:
        affected = scenic_info_service.update_info(info_id, data)
        return ApiResponse.success({"affected_rows": affected}, "更新成功")
    except Exception as e:
        return ApiResponse.error(str(e))

@scenic_bp.route('/info/<int:info_id>', methods=['DELETE'])
def delete_scenic_info(info_id):
    """删除景区概况"""
    try:
        affected = scenic_info_service.delete_info(info_id)
        return ApiResponse.success({"affected_rows": affected}, "删除成功")
    except Exception as e:
        return ApiResponse.error(str(e))