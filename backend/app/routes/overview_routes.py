from flask import jsonify, request
from app.services.overview_service import OverviewService
from . import scenic_bp

overview_service = OverviewService()

@scenic_bp.route('/overview', methods=['GET'])
def get_scenic_info():
    """获取景区全局信息接口"""
    try:
        data = overview_service.get_overview()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@scenic_bp.route('/overview', methods=['POST'])
def add_overview():
    """新增景区概况"""
    data = request.get_json()
    try:
        new_id = overview_service.add_overview(data)
        return jsonify({"status": "success", "data": {"id": new_id}})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@scenic_bp.route('/overview/<int:overview_id>', methods=['PUT'])
def update_overview(overview_id):
    """更新景区概况"""
    data = request.get_json()
    try:
        affected = overview_service.update_overview(overview_id, data)
        return jsonify({"status": "success", "affected_rows": affected})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@scenic_bp.route('/overview/<int:overview_id>', methods=['DELETE'])
def delete_overview(overview_id):
    """删除景区概况"""
    try:
        affected = overview_service.delete_overview(overview_id)
        return jsonify({"status": "success", "affected_rows": affected})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500