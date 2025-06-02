import sqlite3
from ..db.connection import get_connection, close_connection

class Magazine:
    def __init__(self, name, category, id=None):
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
                    magazine = cls(row['name'], row['category'], row['id'])
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
                    magazine = cls(row['name'], row['category'], row['id'])
            except sqlite3.Error as e:
                print(f"Error finding magazine by name: {e}")
            finally:
                close_connection(conn)
        return magazine

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
                    magazines.append(cls(row['name'], row['category'], row['id']))
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
        from .article import Article
        return Article.find_by_magazine_id(self.id)

    def article_titles(self):
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

    def contributing_authors(self): # This method is explicitly called by some tests
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
                from .author import Author
                for row in rows:
                    authors.append(Author(row['name'], row['id']))
            except sqlite3.Error as e:
                print(f"Error getting contributing authors for magazine {self.name}: {e}")
            finally:
                close_connection(conn)
        return authors

    # NEW: Add this method to satisfy tests explicitly calling 'contributors()'
    def contributors(self):
        return self.contributing_authors() # This method simply calls the other one

    @classmethod
    def with_multiple_authors(cls):
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
                    magazines.append(cls(row['name'], row['category'], row['id']))
            except sqlite3.Error as e:
                print(f"Error finding magazines with multiple authors: {e}")
            finally:
                close_connection(conn)
        return magazines

    @classmethod
    def article_counts(cls):
        counts_list = []
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
                    counts_list.append({'name': row['name'], 'article_count': row['article_count']})
            except sqlite3.Error as e:
                print(f"Error getting article counts: {e}")
            finally:
                close_connection(conn)
        return counts_list

