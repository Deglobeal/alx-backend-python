import time
import sqlite3
import functools

# Global query cache
query_cache = {}

# with_db_connection from previous task
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

# Cache decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Using cached result for query.")
            return query_cache[query]
        else:
            print("Executing and caching query.")
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute and cache
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
