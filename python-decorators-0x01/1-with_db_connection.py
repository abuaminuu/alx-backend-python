from functools import functools.wraps
import sqlite3


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
    # If caller supplied a connection explicitly, use it and don't close it here.
	external_connection = kwargs.get("connection", None)
	if external_connection is not None:
		# call the func with with provided connection
		result = func(*args, **kwargs)
    connection = sqlite3.db.connect("users.db")
	try:
	    # Call the wrapped function, injecting the connection as the first argument
    	return func(connection, *args, **kwargs)
    finally:
		# Always close the connection (prevents resource leaks)
        connection.close()
	return wrapper    


# calling decorated function
@with_db_connection 
def get_user_by_id(conn, user_id): 
cursor = conn.cursor() 
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)
