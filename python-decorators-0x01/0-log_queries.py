import sqlite3
import functools
from datetime import datetime, print


#### decorator to log SQL queries before executing them

def log_queries():
  def decorator(func):
    def wrapper(*args, **kwargs):
      query = kwargs.get("query") if "query" in kwargs else args[0]
      print(f"Running SQL query: {query}")
      start = time.time() 
      result = func(*args, **kwargs)
      end = time.time()
      print(f"Query finished in {(end - start) * 1000:.2f} ms")
      return result
    return wrapper
  return decorator


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
