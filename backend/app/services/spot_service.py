from app.utils.db import get_db_connection

class SpotService:
    """景点列表业务逻辑处理"""
    
    def get_scenic_spots_with_flow(self):
        """获取景点列表及其拥挤度状态（联表计算）"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 联表查询：结合 scenic_spots 和 scenic_flow 计算拥挤度
                sql = """
                    SELECT 
                        s.id, s.spot_name, s.en_name, s.description, s.image_url, s.max_capacity, s.sort_order,
                        IFNULL(f.current_visitors, 0) as current_visitors
                    FROM scenic_spots s
                    LEFT JOIN scenic_flow f ON s.id = f.spot_id
                    ORDER BY s.sort_order ASC
                """
                cursor.execute(sql)
                spots = cursor.fetchall()
                
                # 在后端动态计算拥挤度 status
                for spot in spots:
                    ratio = spot['current_visitors'] / spot['max_capacity'] if spot['max_capacity'] > 0 else 0
                    if ratio >= 0.8:
                        spot['status'] = '拥挤'
                    elif ratio >= 0.5:
                        spot['status'] = '适中'
                    else:
                        spot['status'] = '畅通'
                        
                return spots
        finally:
            connection.close()

    def add_spot(self, data):
        """添加新景点"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO scenic_spots 
                    (scenic_id, spot_name, en_name, description, image_url, max_capacity, sort_order)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    data.get('scenic_id', 1), data.get('spot_name'), data.get('en_name'),
                    data.get('description'), data.get('image_url'), data.get('max_capacity', 1000),
                    data.get('sort_order', 0)
                ))
                return cursor.lastrowid
        finally:
            connection.close()

    def update_spot(self, spot_id, data):
        """更新景点信息"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                fields = []
                values = []
                allowed_keys = ['scenic_id', 'spot_name', 'en_name', 'description', 'image_url', 'max_capacity', 'sort_order']
                
                for key in allowed_keys:
                    if key in data:
                        fields.append(f"{key}=%s")
                        values.append(data[key])
                
                if not fields:
                    return 0
                    
                values.append(spot_id)
                sql = f"UPDATE scenic_spots SET {', '.join(fields)} WHERE id=%s"
                cursor.execute(sql, tuple(values))
                return cursor.rowcount
        finally:
            connection.close()

    def delete_spot(self, spot_id):
        """删除景点"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM scenic_spots WHERE id=%s", (spot_id,))
                return cursor.rowcount
        finally:
            connection.close()