from lib.db.connection import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(open("lib/db/schema.sql").read())

    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Alice",))
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Today", "Technology"))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("AI Revolution", 1, 1))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_data()
