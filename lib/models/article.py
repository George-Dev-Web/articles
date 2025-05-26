from lib.db.connection import get_connection

class Article:
    def __init__(self, id, title, author_id, magazine_id):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create(cls, title, author_id, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, author_id, magazine_id)
        )
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return cls(article_id, title, author_id, magazine_id)
