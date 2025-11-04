import time
import sqlite3
from functools import functools.wraps

# retry decorator
def retry_on_failure(retries=3, delay=2):
    """ retry if function raises an exception """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempts in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt: {attemp}, failed: {e}")
                if attempt < retries:
                    print(f"Retrying in {delay} seconds")
                    time.sleep(delay)
                else:
                    print("Max time reached... Giving up")
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
