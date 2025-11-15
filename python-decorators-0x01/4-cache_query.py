import sqlite3
from functools import functools.wraps


query_cache{}

def cache_query(func):
    """ caches SQL query results to avoid redundant database hits """
    @functools.wraps(func)
    def wrapper(connection, *args, **kwargs):
        # identify query strings if supplied as key-args
        query = kwargs.get("query") or (args[0] if args else None)
        # check if result is in the cache
        if query in query_cache:
            print(f"using cache result for query {query}")
            return query_cache[query]
        # otherwise query and store the result
        print(f"⚙️ Executing query and caching result: {query}")
        result = func(connection, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
