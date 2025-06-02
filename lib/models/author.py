# ARTICLES/lib/models/author.py
import sqlite3
from ..db.connection import get_connection, close_connection

class Author:
    def __init__(self, id, name): # The id parameter is required here
        self.id = id
        self.name = name

    # Class method to find an author by ID (already existed, but good to have)
    @classmethod
    def find_by_id(cls, author_id):
        author = None
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM authors WHERE id = ?", (author_id,))
                row = cursor.fetchone()
                if row:
                    author = cls(row['id'], row['name'])
            except sqlite3.Error as e:
                print(f"Error finding author by ID: {e}")
            finally:
                close_connection(conn)
        return author

    # FIX: AttributeError: type object 'Author' has no attribute 'find_by_name'
    @classmethod
    def find_by_name(cls, name):
        author = None
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM authors WHERE name = ?", (name,))
                row = cursor.fetchone()
                if row:
                    author = cls(row['id'], row['name'])
            except sqlite3.Error as e:
                print(f"Error finding author by name: {e}")
            finally:
                close_connection(conn)
        return author

    def save(self):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                if self.id is None:
                    cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
                    self.id = cursor.lastrowid
                else:
                    cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error saving author: {e}")
            finally:
                close_connection(conn)

    def articles(self):
        """
        Retrieves all Article objects associated with this author.
        Uses lazy import to avoid circular dependency.
        """
        from .article import Article # Local import
        return Article.find_by_author_id(self.id)

    # FIX: AttributeError: type object 'Author' has no attribute 'top_author'
    @classmethod
    def top_author(cls):
        """
        Returns the Author object who has written the most articles.
        Returns None if no authors or articles exist.
        """
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT authors.id, authors.name, COUNT(articles.id) as article_count
                    FROM authors
                    JOIN articles ON authors.id = articles.author_id
                    GROUP BY authors.id, authors.name
                    ORDER BY article_count DESC
                    LIMIT 1
                """)
                row = cursor.fetchone()
                if row:
                    return cls(row['id'], row['name'])
            except sqlite3.Error as e:
                print(f"Error finding top author: {e}")
            finally:
                close_connection(conn)
        return None