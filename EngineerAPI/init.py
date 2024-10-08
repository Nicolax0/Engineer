import psycopg2
from psycopg2 import sql
import os

def initialize_database():
    try:
        # connect to postgres DB
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        # Create a cursor object
        cur = conn.cursor()

        # Create table with the specified structure
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            DiscordID BIGINT PRIMARY KEY,
            FullName TEXT,
            rcsID TEXT,
            rin BIGINT,
            roles JSONB
        );
        """
        
        cur.execute(create_table_query)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()
        print("Database initialized successfully.")
        return True
    except Exception as e:
        print(f"An error occurred when initalizing the database: {e}")
        return False