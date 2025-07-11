#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """Generator that yields ages one by one from user_data table"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',    
            password='Dononye12@123',   
            database='ALX_prodev'
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT age FROM user_data")
            for row in cursor:
                yield row['age']
            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error: {e}")

def calculate_average_age():
    """Calculate average age using the stream_user_ages generator"""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count == 0:
        print("Average age of users: No data")
        return
    average = total_age / count
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    calculate_average_age()
