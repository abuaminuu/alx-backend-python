import sys


def stream_user_ages():
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    try:
        # Execute query to fetch ages only
        cursor.execute("SELECT age FROM user_data")

        # Loop once through cursor
        while True:
            # fetch one row at a time
            row = cursor.fetchone()
             # no more rows          
            if row is None:                 
                break
            try:
                row = int(row)
                # send one age at a time
                yield row["age"]
            except ValueError as e:
                print(e)
                sys.exit(1)
    finally:
        cursor.close()
        connection.close()


def calculate_average():
    total_age = 0
    count = 0

    # consuming generator
    for age in stream_user_ages():
        total_age = total_age + age
        count += 1
    
    if count = 0:
        average = 0
    else:
        average = total_age / count
    
    print("averahe of users: ", average)
