from app.utils.db import get_db_connection

class ConfigService:
    """系统配置业务逻辑处理"""
    
    def get_all_config(self):
        """获取所有配置项"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT config_key, config_value, description FROM system_config")
                rows = cursor.fetchall()
                # 转换为字典形式，方便前端直接使用 { "theme": "default", ... }
                config_dict = {row['config_key']: row['config_value'] for row in rows}
                return config_dict
        finally:
            connection.close()

    def get_config(self, key):
        """获取单个配置项"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT config_value FROM system_config WHERE config_key = %s", (key,))
                row = cursor.fetchone()
                return row['config_value'] if row else None
        finally:
            connection.close()

    def update_config(self, key, value):
        """更新单个配置项"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 使用 INSERT ... ON DUPLICATE KEY UPDATE 来实现存在则更新，不存在则插入
                sql = """
                    INSERT INTO system_config (config_key, config_value) 
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE config_value = VALUES(config_value)
                """
                cursor.execute(sql, (key, value))
                connection.commit()
                return True
        finally:
            connection.close()
