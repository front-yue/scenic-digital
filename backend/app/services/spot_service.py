from app.utils.db import get_db_connection

class SpotService:
    """景点列表业务逻辑处理"""
    
    def get_scenic_spots(self):
        """获取景点列表（含经纬度）"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT 
                        id, scenic_id, spot_name, en_name, description, 
                        image_url, latitude, longitude, sort_order
                    FROM scenic_spots
                    ORDER BY sort_order ASC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def add_spot(self, data):
        """添加新景点"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO scenic_spots 
                    (scenic_id, spot_name, en_name, description, image_url, latitude, longitude, sort_order)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    data.get('scenic_id', 1), data.get('spot_name'), data.get('en_name'),
                    data.get('description'), data.get('image_url'),
                    data.get('latitude'), data.get('longitude'),
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
                allowed_keys = ['scenic_id', 'spot_name', 'en_name', 'description', 'image_url', 'latitude', 'longitude', 'sort_order']
                
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
