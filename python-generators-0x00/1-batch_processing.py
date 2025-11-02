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
    batch_size = 10
    rows = stream_users_in_batches(batch_size)
    for row in rows:
        age = row.get("age")
        if age and int(age) > 25:
            yield row
    
