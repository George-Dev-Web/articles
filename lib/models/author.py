import sqlite3
from ..db.connection import get_connection, close_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

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
                    author = cls(row['name'], row['id'])
            except sqlite3.Error as e:
                print(f"Error finding author by ID: {e}")
            finally:
                close_connection(conn)
        return author

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
                    author = cls(row['name'], row['id'])
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
        from .article import Article
        return Article.find_by_author_id(self.id)

    def magazines(self):
        from .magazine import Magazine
        conn = get_connection()
        magazines_list = []
        if conn and self.id is not None:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT magazines.id, magazines.name, magazines.category
                    FROM magazines
                    JOIN articles ON magazines.id = articles.magazine_id
                    WHERE articles.author_id = ?
                """, (self.id,))
                rows = cursor.fetchall()
                for row in rows:
                    magazines_list.append(Magazine(row['name'], row['category'], row['id']))
            except sqlite3.Error as e:
                print(f"Error finding magazines for author: {e}")
            finally:
                close_connection(conn)
        return magazines_list

    def add_article(self, magazine, title, content=""): # TWEAK: content now has a default value
        from .article import Article
        if self.id is None or magazine.id is None:
            print("Author or Magazine must be saved to add an article.")
            return None
        article = Article(title, content, self.id, magazine.id)
        article.save()
        return article

    @classmethod
    def top_author(cls):
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
                    return cls(row['name'], row['id'])
            except sqlite3.Error as e:
                print(f"Error finding top author: {e}")
            finally:
                close_connection(conn)
        return None

