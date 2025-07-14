import sqlite3
import functools 

# Decorator to cache query results
def log_query(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        # Connect to the database
        print(f"Executiom SQI Query: {query}")
        return function(query, *args, **kwargs)
    return wrapper
@log_query
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")