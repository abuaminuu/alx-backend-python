import sqlite3

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
        
            
