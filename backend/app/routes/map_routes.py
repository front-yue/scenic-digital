from flask import Blueprint, request, current_app
import urllib.parse
import urllib.request
import json
from app.utils.response import ApiResponse

map_bp = Blueprint('map', __name__)

@map_bp.route('/geocode', methods=['GET'])
def geocode():
    """
    将地点名称转换为经纬度坐标的接口
    GET /api/map/geocode?address=xxx
    """
    address = request.args.get('address')
    if not address:
        return ApiResponse.error(message='缺少地址参数 address', code=400)

    amap_key = current_app.config.get('AMAP_KEY')
    if not amap_key:
        return ApiResponse.error(message='服务器未配置高德地图 API Key', code=500)

    try:
        url = f"https://restapi.amap.com/v3/geocode/geo?address={urllib.parse.quote(address)}&city={urllib.parse.quote('全国')}&key={amap_key}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get('status') == '1' and res_data.get('geocodes') and len(res_data['geocodes']) > 0:
                location = res_data['geocodes'][0]['location']
                return ApiResponse.success(data={'location': location}, message='获取经纬度成功')
            else:
                return ApiResponse.error(message=f"高德 API 未返回有效坐标: {res_data.get('info')}", code=404)
    except Exception as e:
        return ApiResponse.error(message=f'获取经纬度发生异常: {str(e)}', code=500)