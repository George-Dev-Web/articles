# ARTICLES/lib/models/magazine.py
import sqlite3
from ..db.connection import get_connection, close_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def find_by_id(cls, magazine_id):
        magazine = None
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, category FROM magazines WHERE id = ?", (magazine_id,))
                row = cursor.fetchone()
                if row:
                    magazine = cls(row['id'], row['name'], row['category'])
            except sqlite3.Error as e:
                print(f"Error finding magazine by ID: {e}")
            finally:
                close_connection(conn)
        return magazine

    @classmethod
    def find_by_name(cls, name):
        magazine = None
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, category FROM magazines WHERE name = ?", (name,))
                row = cursor.fetchone()
                if row:
                    magazine = cls(row['id'], row['name'], row['category'])
            except sqlite3.Error as e:
                print(f"Error finding magazine by name: {e}")
            finally:
                close_connection(conn)
        return magazine

    # FIX: AttributeError: type object 'Magazine' has no attribute 'find_by_category'
    @classmethod
    def find_by_category(cls, category):
        magazines = []
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, category FROM magazines WHERE category = ?", (category,))
                rows = cursor.fetchall()
                for row in rows:
                    magazines.append(cls(row['id'], row['name'], row['category']))
            except sqlite3.Error as e:
                print(f"Error finding magazines by category: {e}")
            finally:
                close_connection(conn)
        return magazines

    def save(self):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                if self.id is None:
                    cursor.execute(
                        "INSERT INTO magazines (name, category) VALUES (?, ?)",
                        (self.name, self.category)
                    )
                    self.id = cursor.lastrowid
                else:
                    cursor.execute(
                        "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                        (self.name, self.category, self.id)
                    )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error saving magazine: {e}")
            finally:
                close_connection(conn)

    def articles(self):
        """
        Retrieves all Article objects associated with this magazine.
        Uses lazy import to avoid circular dependency.
        """
        from .article import Article # Local import
        return Article.find_by_magazine_id(self.id)

    # FIX: AttributeError: 'Magazine' object has no attribute 'article_titles'
    def article_titles(self):
        """Returns a list of titles of all articles belonging to this magazine."""
        titles = []
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
                rows = cursor.fetchall()
                titles = [row['title'] for row in rows]
            except sqlite3.Error as e:
                print(f"Error getting article titles for magazine {self.name}: {e}")
            finally:
                close_connection(conn)
        return titles

    # FIX: AttributeError: 'Magazine' object has no attribute 'contributing_authors'
    def contributing_authors(self):
        """
        Returns a list of unique Author objects who have contributed to this magazine.
        Returns None if no authors have contributed.
        """
        authors = []
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT authors.id, authors.name
                    FROM authors
                    JOIN articles ON authors.id = articles.author_id
                    WHERE articles.magazine_id = ?
                """, (self.id,))
                rows = cursor.fetchall()
                from .author import Author # Local import
                for row in rows:
                    authors.append(Author(row['id'], row['name']))
            except sqlite3.Error as e:
                print(f"Error getting contributing authors for magazine {self.name}: {e}")
            finally:
                close_connection(conn)
        # As per the requirements, if no authors, return None
        return authors if authors else None

    # FIX: AttributeError: type object 'Magazine' has no attribute 'with_multiple_authors'
    @classmethod
    def with_multiple_authors(cls):
        """
        Returns a list of Magazine objects that have more than one contributing author.
        """
        magazines = []
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT magazines.id, magazines.name, magazines.category
                    FROM magazines
                    JOIN articles ON magazines.id = articles.magazine_id
                    GROUP BY magazines.id, magazines.name, magazines.category
                    HAVING COUNT(DISTINCT articles.author_id) > 1
                """)
                rows = cursor.fetchall()
                for row in rows:
                    magazines.append(cls(row['id'], row['name'], row['category']))
            except sqlite3.Error as e:
                print(f"Error finding magazines with multiple authors: {e}")
            finally:
                close_connection(conn)
        return magazines

    # FIX: AttributeError: type object 'Magazine' has no attribute 'article_counts'
    @classmethod
    def article_counts(cls):
        """
        Returns a dictionary where keys are magazine names and values are the count of articles.
        """
        counts = {}
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT magazines.name, COUNT(articles.id) AS article_count
                    FROM magazines
                    LEFT JOIN articles ON magazines.id = articles.magazine_id
                    GROUP BY magazines.name
                """)
                rows = cursor.fetchall()
                for row in rows:
                    counts[row['name']] = row['article_count']
            except sqlite3.Error as e:
                print(f"Error getting article counts: {e}")
            finally:
                close_connection(conn)
        return counts