import sys
from mysql.connection import Error
from .. import seed


# Write a function  that fetches rows in batches
def stream_users_in_batches(batch_size):

    # convert batch size to int
    try:
        batch_size = int(batch_size)
    except ValueError as e:
        print(e)
        sys.exit(1)

    # connect to the database
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM user_data")
        while True:
            # fetch data from users table in batches
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            for row in rows:
                yield row
    except Error as e:
        print(f"database error {e}")
    finally:
        # terminate connection
        cursor.close()
        connection.close()


# Write a function  that processes each batch to filter users over the age of 25
def batch_processing():

    # connect to the database
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    batch_size = 15
    try:
        # filter data from users table with age > 25
        cursor.execute("SELECT * FROM user_data WHERE age > 25")
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        return rows
    except Error as e:
        print(f"error fetching data{e}")
    finally:
        # terminate connection
        cursor.close()
        connection.close()


# Implement a generator function  that implements the
# paginate_users(page_size, offset) that will only fetch
# the next page when needed at an offset of 0.
def paginate_users(page_size, offset):

    # connect to databse
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    # execute one query
    query = "SELECT * FROM user_data ORDER BY user_id LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))

    # returns up to page_size rows
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # to avoid injection and leaks
    return rows


def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        # update offset to next page
        offset = offset + page_size
