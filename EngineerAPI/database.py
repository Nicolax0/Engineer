import psycopg2
from psycopg2 import sql
import os

def connect_to_db():
    try:
        # Establish the connection
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        print("Connection to PostgreSQL DB successful")
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL DB: {e}")
        return None

# Example usage
# connection = connect_to_db(host='localhost', database='mydb', user='myuser', password='mypassword')