import mysql.connector
from mysql.connector import Error
import csv
import uuid

def connect_db():
    """Connects to the MySQL server."""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='Dononye12@123'
        )
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None

def create_database(connection):
    """Creates the ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='Dononye12@123',
            database='ALX_prodev'
        )
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection):
    """Creates the user_data table if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            )
        """)
        print("Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, csv_file):
    """Inserts user data from a CSV file into the user_data table."""
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE user_id = user_id
                """, (str(uuid.uuid4()), row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found.")

def stream_users(connection):
    """Generator that yields one user row at a time from the user_data table."""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
        cursor.close()
    except Error as e:
        print(f"Error streaming users: {e}")




if __name__ == "__main__":
    conn = connect_db()
    if conn:
        print("Connection to MySQL successful.")
        create_database(conn)
        conn.close()

        conn = connect_to_prodev()
        if conn:
            create_table(conn)
            insert_data(conn, "user_data.csv")
            print("Inserted data successfully. Sample rows:")

            # Print 5 rows using generator
            count = 0
            for row in stream_users(conn):
                print(row)
                count += 1
                if count >= 5:
                    break

            conn.close()

