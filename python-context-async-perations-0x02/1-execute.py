import sqlite3

class ExecuteQuery():

    def __init__(self, user.db, query, params=None) -> None:
        self.user_db = user.db
        self.query = query
        self.params = params or ()
        self.connection = None
        self.results = None

    def __enter__(self):
        # Open the connection (sqlite3.connect)
        self.connection = sqlite3.connect(self.user_db)
        # Create a cursor
        cursor = self.connection.cursor()
        # Execute the query with its parameters (if any)
        cursor.execute(self.query)        
        # Fetch the results
        self.results = cursor.fetchall()
        # Return the results to the with block
        return self.results

    def __exit__(self, exception_value, exception_type, traceback):
        # commint when no error
        if exception is None:
            self.connection.commit()
        else:
            # rollback
            self.connection.rollback()
        # close connection
        self.connection.close()
        # propagate exception if needed
        return False

# Example usage
with ExecuteQuery("users.db", "SELECT * FROM users WHERE age > ?", (25,)) as results:
    print("Users older than 25:")
    for user in results:
        print(user)
