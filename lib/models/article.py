# ARTICLES/lib/models/article.py
import sqlite3
from ..db.connection import get_connection, close_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def find_by_author_id(cls, author_id):
        articles = []
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, title, content, author_id, magazine_id FROM articles WHERE author_id = ?", (author_id,))
                rows = cursor.fetchall()
                for row in rows:
                    articles.append(cls(
                        row['id'], row['title'], row['content'], row['author_id'], row['magazine_id']
                    ))
            except sqlite3.Error as e:
                print(f"Error finding articles by author ID: {e}")
            finally:
                close_connection(conn)
        return articles

    # FIX: AttributeError: type object 'Article' has no attribute 'find_by_title'
    @classmethod
    def find_by_title(cls, title):
        article = None
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, title, content, author_id, magazine_id FROM articles WHERE title = ?", (title,))
                row = cursor.fetchone()
                if row:
                    article = cls(
                        row['id'], row['title'], row['content'], row['author_id'], row['magazine_id']
                    )
            except sqlite3.Error as e:
                print(f"Error finding article by title: {e}")
            finally:
                close_connection(conn)
        return article

    # New method needed for Magazine.articles()
    @classmethod
    def find_by_magazine_id(cls, magazine_id):
        articles = []
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, title, content, author_id, magazine_id FROM articles WHERE magazine_id = ?", (magazine_id,))
                rows = cursor.fetchall()
                for row in rows:
                    articles.append(cls(
                        row['id'], row['title'], row['content'], row['author_id'], row['magazine_id']
                    ))
            except sqlite3.Error as e:
                print(f"Error finding articles by magazine ID: {e}")
            finally:
                close_connection(conn)
        return articles

    def save(self):
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                if self.id is None:
                    cursor.execute(
                        "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                        (self.title, self.content, self.author_id, self.magazine_id)
                    )
                    self.id = cursor.lastrowid
                else:
                    cursor.execute(
                        "UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                        (self.title, self.content, self.author_id, self.magazine_id, self.id)
                    )
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error saving article: {e}")
            finally:
                close_connection(conn)

    def magazine(self):
        from .magazine import Magazine # Local import
        return Magazine.find_by_id(self.magazine_id)

    def author(self):
        from .author import Author # Local import
        return Author.find_by_id(self.author_id)