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
        cursor.execute("SELECT * FROM user_table")
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
        cursor.execute("SELECT * FROM user_table WHERE age > 25")
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows
    except Error as e:
        print(f"error fetching data{e}")
    finally:
        # terminate connection
        cursor.close()
        connection.close()

