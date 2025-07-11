import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that connects to ALX_prodev and yields users one by one"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Dononye12@123',
            database='ALX_prodev'
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")
            for row in cursor:
                yield row
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error: {e}")
