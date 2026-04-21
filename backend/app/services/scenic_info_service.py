from app.utils.db import get_db_connection

class ScenicInfoService:
    """景区概况业务逻辑处理"""
    
    def get_info(self):
        """获取景区全局信息"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM scenic_info LIMIT 1")
                return cursor.fetchone()
        finally:
            connection.close()

    def add_info(self, data):
        """添加景区概况"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO scenic_info 
                    (scenic_name, scenic_en_name, cover_image, weather_temp, weather_desc, introduction, ticket_price, opening_hours, address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    data.get('scenic_name'), data.get('scenic_en_name'), data.get('cover_image'),
                    data.get('weather_temp'), data.get('weather_desc'), data.get('introduction'),
                    data.get('ticket_price'), data.get('opening_hours'), data.get('address')
                ))
                return cursor.lastrowid
        finally:
            connection.close()

    def update_info(self, info_id, data):
        """更新景区概况"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                fields = []
                values = []
                allowed_keys = ['scenic_name', 'scenic_en_name', 'cover_image', 'weather_temp', 'weather_desc', 'introduction', 'ticket_price', 'opening_hours', 'address']
                
                for key in allowed_keys:
                    if key in data:
                        fields.append(f"{key}=%s")
                        values.append(data[key])
                
                if not fields:
                    return 0
                    
                values.append(info_id)
                sql = f"UPDATE scenic_info SET {', '.join(fields)} WHERE id=%s"
                cursor.execute(sql, tuple(values))
                return cursor.rowcount
        finally:
            connection.close()

    def delete_info(self, info_id):
        """删除景区概况"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM scenic_info WHERE id=%s", (info_id,))
                return cursor.rowcount
        finally:
            connection.close()