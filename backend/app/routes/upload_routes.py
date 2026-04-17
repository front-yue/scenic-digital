from flask import Blueprint, request, current_app, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from app.utils.response import ApiResponse

upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    """检查文件扩展名是否被允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@upload_bp.route('/upload', methods=['POST'])
def upload_image():
    """
    通用图片上传接口
    接收表单中的 file 字段
    返回可直接访问的图片 URL
    """
    # 1. 检查请求中是否包含文件
    if 'file' not in request.files:
        return ApiResponse.error("没有找到文件字段(file)", code=400)
    
    file = request.files['file']
    
    # 2. 检查用户是否选择了文件
    if file.filename == '':
        return ApiResponse.error("没有选择文件", code=400)
        
    # 3. 检查文件类型是否合法
    if file and allowed_file(file.filename):
        try:
            # 提取原文件后缀
            ext = file.filename.rsplit('.', 1)[1].lower()
            
            # 使用 UUID 生成唯一的文件名，防止重名覆盖和中文名乱码问题
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            
            # 构建保存路径并保存
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(save_path)
            
            # 构建并返回完整的访问 URL
            # 假设后端运行在 8888 端口，返回如 http://127.0.0.1:8888/uploads/xxx.png
            file_url = request.host_url.rstrip('/') + f"/uploads/{unique_filename}"
            
            return ApiResponse.success({
                "url": file_url,
                "filename": unique_filename
            }, message="图片上传成功")
            
        except Exception as e:
            return ApiResponse.error(f"图片保存失败: {str(e)}")
            
    return ApiResponse.error("不支持的文件类型", code=400)
