import sqlite3


# custom context manager DatabaseConnection using the __enter__ and the __exit__ methods
class DatabaseConnection():
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        
    def __enter__(self):
        connection = sqlite3.connect(self.db_name)
        self.connection = connection
        return self.connection

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is None:
            # commit the changes
            self.connection.commit()
        else:
            # rollback the ops keep the data consistent
            self.connection.rollback()
        # close the connection anyway
        self.connection.close()
        # propagate exception if needed
        return False

# Use the context manager with the with statement to be able to perform the query SELECT * FROM users. Print the results from the query.
def query_database(db_name):
    try:
        with DatabaseConnection(db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            for row in results:
                print(row)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

# Example usage
query_database('example.db')
            
