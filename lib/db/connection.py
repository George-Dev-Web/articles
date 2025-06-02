# ARTICLES/lib/db/connection.py
import sqlite3
import os

# Get the absolute path of the directory containing connection.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up two levels to reach the ARTICLES/ root directory
# (from lib/db/ to lib/, then from lib/ to ARTICLES/)
project_root = os.path.join(current_dir, '..', '..')

# Define the full path to articles.db, assuming it's in the ARTICLES/ root
DATABASE_NAME = os.path.join(project_root, "articles.db")

# --- THIS IS THE CRITICAL DEBUG PRINT. ENSURE IT'S THERE. ---
print(f"DEBUG: DATABASE_NAME (absolute path) = {DATABASE_NAME}")
# --- END CRITICAL DEBUG PRINT ---

def get_connection():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        # --- MAKE SURE THIS PRINT IS ALSO THERE ---
        print(f"Attempted to connect to: {DATABASE_NAME}")
        # --- END CHECK ---
        return None

def close_connection(conn):
    if conn:
        conn.close()

def create_tables():
    conn = get_connection()
    if conn: # Check if connection was successful
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL, -- This line is vital
                    author_id INTEGER NOT NULL,
                    magazine_id INTEGER NOT NULL,
                    FOREIGN KEY (author_id) REFERENCES authors(id),
                    FOREIGN KEY (magazine_id) REFERENCES magazines(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS authors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS magazines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL
                )
            """)
            conn.commit()
            print("Tables created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
        finally:
            close_connection(conn)
    else: # Added a message if connection failed
        print("Skipping table creation: Database connection failed.")