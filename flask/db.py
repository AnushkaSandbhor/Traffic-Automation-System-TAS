import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()  # This will load the .env file
 
 
# MySQL connection details from .env
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}
 
SECRET_KEY = os.getenv('SECRET_KEY')
 
def get_db_connection():
    #Database connection function
    try:
        print(f"Connecting to MySQL database at {db_config['host']}...")
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None
 
if __name__ == "__main__":
    connection = get_db_connection()
    if connection:
        connection.close()
        print("Database connection closed")
    else:
        print("Failed to connect to the database")
 