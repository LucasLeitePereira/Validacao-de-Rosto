import psycopg2
from config import DB_CONFIG

def get_db_connection():
    """Establishes and returns a database connection and cursor."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("Database connection established.")
        return conn, cur
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None, None

def close_db_connection(conn, cur):
    """Closes the database connection and cursor."""
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("Database connection closed.")
