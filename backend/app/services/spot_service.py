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
                        spot['status'] = '拥挤预警'
                    elif ratio >= 0.5:
                        spot['status'] = '轻微拥挤'
                    else:
                        spot['status'] = '良好畅通'
                        
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
                connection.commit()
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
                connection.commit()
                return cursor.rowcount
        finally:
            connection.close()

    def delete_spot(self, spot_id):
        """删除景点"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM scenic_spots WHERE id=%s", (spot_id,))
                connection.commit()
                return cursor.rowcount
        finally:
            connection.close()

    def update_flow(self, spot_id, current_visitors):
        """更新景点客流（模拟）"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 尝试更新
                cursor.execute("UPDATE scenic_flow SET current_visitors=%s, recorded_at=CURRENT_TIMESTAMP WHERE spot_id=%s", (current_visitors, spot_id))
                if cursor.rowcount == 0:
                    # 如果不存在则插入
                    cursor.execute("INSERT INTO scenic_flow (spot_id, current_visitors) VALUES (%s, %s)", (spot_id, current_visitors))
                connection.commit()
                return True
        finally:
            connection.close()