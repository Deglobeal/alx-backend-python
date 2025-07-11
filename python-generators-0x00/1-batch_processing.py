import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches from the user_data table.
    Yields each batch of users (as a list of dictionaries).
    """
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
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error: {e}")

def batch_processing(batch_size):
    """
    Processes each batch of users and prints only users with age > 25.
    Uses only 2 loops: one for batches, one for users in batch.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
