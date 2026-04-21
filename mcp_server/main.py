import os
import json
import urllib.parse
import urllib.request
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# 加载 .env 配置文件
load_dotenv()

# 初始化一个名为 ScenicMapServer 的 MCP 服务
mcp = FastMCP("ScenicMapServer")

AMAP_KEY = os.environ.get("AMAP_KEY", "")
BACKEND_API_URL = os.environ.get("BACKEND_API_URL", "")

def get_location_coordinate(address: str) -> str:
    """内部辅助函数：将地点名称转换为经纬度坐标"""
    try:
        # 添加 city=全国 参数，避免在高德某些默认配置下跨城搜索失败
        url = f"https://restapi.amap.com/v3/geocode/geo?address={urllib.parse.quote(address)}&city={urllib.parse.quote('全国')}&key={AMAP_KEY}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get('status') == '1' and res_data.get('geocodes') and len(res_data['geocodes']) > 0:
                return res_data['geocodes'][0]['location']
            else:
                print(f"高德 API 返回数据不包含 geocodes: {res_data}")
    except Exception as e:
        print(f"获取经纬度失败: {e}")
    return None

def get_current_scenic_address() -> str:
    """从本地后端 API 获取当前景区的地理位置"""
    try:
        url = f"{BACKEND_API_URL}/scenic/info"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            res_data = response.json()
            if res_data.get('code') == 200 and res_data.get('data'):
                return res_data['data'].get('address')
    except Exception as e:
        print(f"获取景区位置失败: {e}")
    return None


@mcp.tool()
def get_map_route(start_point: str, end_point: str) -> str:
    """
    调用高德地图 API 获取两点之间的步行导航路线。
    
    Args:
        start_point: 起点名称 (例如：景区南门、云海观景台)。如果用户说“从这里”、“当前位置”、“我这里”、“这儿”等，必须传入默认值“当前位置”。
        end_point: 终点名称 (例如：千年古刹、洗手间、浙江大学湖州研究院)
        
    Returns:
        一段自然语言描述的步行导航路线和预计时间
    """
    # 0. 智能处理“当前位置”
    display_start_point = start_point
    if any(keyword in start_point for keyword in ["从这里", "当前位置", "我这里", "这儿"]):
        start_point = get_current_scenic_address()
        if not start_point:
            return "抱歉，我无法获取当前景区的地理位置，请联系管理员。"
        display_start_point = "当前位置"

    # 1. 将起点和终点转换为经纬度
    if not AMAP_KEY:
        return "抱歉，MCP 服务器未配置高德地图 API Key，无法使用导航功能。"
        
    origin_coord = get_location_coordinate(start_point)
    dest_coord = get_location_coordinate(end_point)
    
    if not origin_coord or not dest_coord:
        return f"抱歉，我无法在地图上准确定位【{display_start_point}】或【{end_point}】，请提供更具体的地点名称。"
        
    # 2. 调用高德步行路径规划 API
    try:
        url = f"https://restapi.amap.com/v3/direction/walking?origin={origin_coord}&destination={dest_coord}&key={AMAP_KEY}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            route_data = json.loads(response.read().decode('utf-8'))
            
            if route_data.get('status') == '1' and route_data.get('route') and route_data['route'].get('paths'):
                path = route_data['route']['paths'][0]
                distance = int(path.get('distance', 0))
                duration = int(path.get('duration', 0)) // 60 # 转换为分钟
                
                # 提取前几个关键的步行指令
                steps = path.get('steps', [])
                instructions = [step.get('instruction', '') for step in steps[:3]]
                instruction_text = "，然后".join(instructions)
                
                # 去除返回结果中的换行符，让 Fay 的大模型解析更稳定
                result = f"为您规划了从【{display_start_point}】到【{end_point}】的路线：全程大约 {distance} 米，预计需要 {duration} 分钟。主要路线：{instruction_text}。"
                return result
            else:
                # 增加对驾车/公交的兼容提示
                return f"抱歉，【{display_start_point}】到【{end_point}】距离可能过远，超出了步行导航的范围，建议您使用地图 APP 选择驾车或公交出行。"
    except Exception as e:
        return f"查询路线时发生网络错误，请稍后再试。"

if __name__ == "__main__":
    # 使用标准输入输出(stdio)运行 MCP Server
    # 这样可以被 Fay 的 LLM 引擎通过管道调用
    mcp.run(transport='stdio')
