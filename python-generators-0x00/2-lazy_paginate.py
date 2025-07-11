#!/usr/bin/python3
seed = __import__('seed')

def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database with LIMIT and OFFSET.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator that lazily fetches pages of users with the given page_size.
    Uses only one loop and yields pages as lists of user dicts.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
