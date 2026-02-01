import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="Class_GPA_Management_SYS_db",
        charset='utf8mb4',
    )
