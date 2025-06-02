# ARTICLES/lib/db/connection.py
import sqlite3

DATABASE_NAME = "articles.db" # Adjust path as needed

def get_connection():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def close_connection(conn):
    if conn:
        conn.close()

def create_tables():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
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