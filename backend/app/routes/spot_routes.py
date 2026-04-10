from flask import request
from app.services.spot_service import SpotService
from app.utils.response import ApiResponse
from . import scenic_bp

spot_service = SpotService()

@scenic_bp.route('/spots', methods=['GET'])
def get_scenic_spots():
    """获取景点及客流状态接口"""
    try:
        data = spot_service.get_scenic_spots_with_flow()
        return ApiResponse.success(data)
    except Exception as e:
        return ApiResponse.error(str(e))

@scenic_bp.route('/spots', methods=['POST'])
def add_spot():
    """新增景点"""
    data = request.get_json()
    try:
        new_id = spot_service.add_spot(data)
        return ApiResponse.success({"id": new_id}, "新增成功")
    except Exception as e:
        return ApiResponse.error(str(e))

@scenic_bp.route('/spots/<int:spot_id>', methods=['PUT'])
def update_spot(spot_id):
    """更新景点信息"""
    data = request.get_json()
    try:
        affected = spot_service.update_spot(spot_id, data)
        return ApiResponse.success({"affected_rows": affected}, "更新成功")
    except Exception as e:
        return ApiResponse.error(str(e))

@scenic_bp.route('/spots/<int:spot_id>', methods=['DELETE'])
def delete_spot(spot_id):
    """删除景点"""
    try:
        affected = spot_service.delete_spot(spot_id)
        return ApiResponse.success({"affected_rows": affected}, "删除成功")
    except Exception as e:
        return ApiResponse.error(str(e))