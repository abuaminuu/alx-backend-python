# powering the backend
import mysql.connector
import csv
from mysql.connector import Error

# connects to the mysql database server
def connect_db() :

    # handle error from onset
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="user",
            passwd="password"
        )
        if connection.is_connected():
            print("✅ Connected to MySQL successfully!")
            return connection
    except Error as e:
        print(f"❌ Connection error: {e}❌")
        return None


# creates the database ALX_prodev if it does not exist
def create_database(connection):

    # try to connect
    try:
        # connect first
        connection = connect_db()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
            print("✅ Database 'ALX_prodev' checked/created successfully!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            # close connection
            cursor.close()
            connection.close()
            print("🔒 MySQL connection closed.")



# connects the the ALX_prodev database in MYSQL
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="user",          
            password="password",  
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("✅ Connected to 'ALX_prodev' database successfully!")
            return connection
    except Error as e:
        print("❌ Error while connecting to 'ALX_prodev':", e)
        return None




# creates a table user_data if it does not exists with the required fields
def create_table(cursor):

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="user",
            password="password",  
            database="ALX_prodev"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data(
            user_id INT AUTO INCREMENT Primary Key,
            name VARCHAR(32) NOT NULL UNIQUE,
            email VARCHAR(32) NOT NULL,
            age INT NOT NULL 
            ) 
        """)
        print("✅ Table 'user_data' checked/created successfully!")
    except Error as e:
        print("❌ Error while creating table:", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔒 MySQL connection closed.")


# inserts data in the database if it does not exist
def insert_data(connection, data):
    csv_file_path = "/user_data.csv"

    try:
        # Connect to the existing database
        connection = mysql.connector.connect(
            host="localhost",
            user="user",          # <-- replace with your MySQL username
            password="password",  # <-- replace with your MySQL password
            database="ALX_prodev"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            with open(csv_file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row["name"]
                    email = row["email"]
                    age = int(row["age"])

                    # insert operation with parameterized queries to avoid SQL injection
                    query = """
                    INSERT INTO user_data (name, email, age) 
                    VALUES (%s, %s, %s)
                    """
                    try:
                        cursor.execute(query, (name, email, age))
                    except mysql.connector.IntegrityError as e:
                        # Handle duplicate names (UNIQUE constraint)
                        print(f"⚠️ Skipping duplicate: {email}, {e}")
                        continue
            # commit changes to the database
            connection.commit()
            print("✅ CSV data inserted successfully!")

    except Error as e:
        print(f"error inserting data to thr database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔒 MySQL connection closed.")


