from flask import jsonify

class ApiResponse:
    """统一的 API 响应封装类"""
    
    @staticmethod
    def success(data=None, message="操作成功"):
        """
        成功响应格式
        :param data: 返回的数据
        :param message: 提示信息
        :return: Response, 状态码
        """
        response = {
            "status": "success",
            "code": 200,
            "message": message,
            "data": data
        }
        return jsonify(response), 200

    @staticmethod
    def error(message="操作失败", code=500, data=None):
        """
        错误响应格式
        :param message: 错误提示信息
        :param code: 错误状态码 (默认为 500)
        :param data: 附加错误数据
        :return: Response, 状态码
        """
        response = {
            "status": "error",
            "code": code,
            "message": message,
            "data": data
        }
        return jsonify(response), code
