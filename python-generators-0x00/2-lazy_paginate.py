from mysql.connector import Error
import sys


# Implement a generator function  that implements the
# paginate_users(page_size, offset) that will only fetch
# the next page when needed at an offset of 0.
def paginate_users(page_size, offset):

    # connect to databse
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    try:
        # execute one query
        query = "SELECT * FROM user_data ORDER BY user_id LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))

        # returns up to page_size rows
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        # to avoid leaks and injection
        return rows
    except Error as e:
        print(e)
        sys.exit(1)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# implements lazy paginate
def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        # update offset to next page
        offset = offset + page_size
