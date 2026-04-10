import pymysql
from flask import current_app

def get_db_connection():
    """获取数据库连接对象"""
    return pymysql.connect(
        host=current_app.config['DB_HOST'],
        port=current_app.config['DB_PORT'],
        user=current_app.config['DB_USER'],
        password=current_app.config['DB_PASSWORD'],
        database=current_app.config['DB_NAME'],
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )