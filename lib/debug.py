# ARTICLES/debug.py (AFTER moving it to the root)

# No need for sys.path.append if you run from the project root
# import sys
# import os

# Correct absolute imports from the project root
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.db.connection import create_tables, get_connection, close_connection

# Add import sqlite3 if you directly use sqlite3 in debug.py,
# though the current debug.py typically doesn't directly use it
import sqlite3 # <--- Add this if Pylance keeps complaining about it, though it might be a false positive if you don't use it directly here.

def setup_initial_data():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Clear existing data for a fresh start (optional)
            cursor.execute("DELETE FROM articles")
            cursor.execute("DELETE FROM magazines")
            cursor.execute("DELETE FROM authors")
            conn.commit()

            # Create authors
            author1 = Author(id=None, name="Jane Doe")
            author1.save()
            print(f"Created author: {author1.name} with ID: {author1.id}")

            author2 = Author(id=None, name="John Smith")
            author2.save()
            print(f"Created author: {author2.name} with ID: {author2.id}")

            author3 = Author(id=None, name="Emily White")
            author3.save()
            print(f"Created author: {author3.name} with ID: {author3.id}")

            # Create magazines
            magazine1 = Magazine(id=None, name="Tech Innovators", category="Technology")
            magazine1.save()
            print(f"Created magazine: {magazine1.name} with ID: {magazine1.id}")

            magazine2 = Magazine(id=None, name="Cooking Delights", category="Food")
            magazine2.save()
            print(f"Created magazine: {magazine2.name} with ID: {magazine2.id}")

            magazine3 = Magazine(id=None, name="Global News", category="Current Events")
            magazine3.save()
            print(f"Created magazine: {magazine3.name} with ID: {magazine3.id}")

            # Create articles
            article1 = Article(id=None, title="The Future of AI", content="AI is transforming...", author_id=author1.id, magazine_id=magazine1.id)
            article1.save()

            article2 = Article(id=None, title="Machine Learning Explained", content="A deep dive into ML...", author_id=author1.id, magazine_id=magazine1.id)
            article2.save()

            article3 = Article(id=None, title="Delicious Pasta Recipes", content="Easy and quick pasta...", author_id=author2.id, magazine_id=magazine2.id)
            article3.save()

            article4 = Article(id=None, title="Quantum Computing Basics", content="Introduction to QC...", author_id=author2.id, magazine_id=magazine1.id) # Mag1 has 2 authors now
            article4.save()

            article5 = Article(id=None, title="Breaking News: Event X", content="Details of Event X...", author_id=author3.id, magazine_id=magazine3.id)
            article5.save()

            article6 = Article(id=None, title="Advanced AI Concepts", content="Beyond the basics...", author_id=author3.id, magazine_id=magazine1.id) # Mag1 has 3 authors now
            article6.save()

            print("Initial data setup complete.")

        except sqlite3.Error as e:
            print(f"Error setting up initial data: {e}")
        finally:
            close_connection(conn)

if __name__ == "__main__":
    print("Initializing database tables...")
    create_tables() # Ensure tables exist

    print("\nSetting up initial data...")
    setup_initial_data()

    print("\n--- Testing Article lookups ---")
    found_article = Article.find_by_title("The Future of AI")
    if found_article:
        print(f"Found article by title: '{found_article.title}'")
        print(f"  Associated Magazine: {found_article.magazine().name}")
        print(f"  Associated Author: {found_article.author().name}")
    else:
        print("Article 'The Future of AI' not found.")

    print("\n--- Testing Author methods ---")
    jane_doe = Author.find_by_name("Jane Doe")
    if jane_doe:
        print(f"Found author by name: {jane_doe.name} (ID: {jane_doe.id})")
        print(f"Articles by {jane_doe.name}:")
        for article in jane_doe.articles():
            print(f"- {article.title}")
    else:
        print("Author 'Jane Doe' not found.")

    top_author = Author.top_author()
    if top_author:
        print(f"\nTop Author: {top_author.name} (ID: {top_author.id})")
    else:
        print("\nNo top author found.")

    print("\n--- Testing Magazine methods ---")
    tech_magazines = Magazine.find_by_category("Technology")
    print("\nMagazines in 'Technology' category:")
    for mag in tech_magazines:
        print(f"- {mag.name}")

    tech_innovators = Magazine.find_by_name("Tech Innovators")
    if tech_innovators:
        print(f"\nArticle titles in '{tech_innovators.name}': {tech_innovators.article_titles()}")

        contributing_authors = tech_innovators.contributing_authors()
        if contributing_authors:
            print(f"Contributing authors for '{tech_innovators.name}': {[a.name for a in contributing_authors]}")
        else:
            print(f"No contributing authors for '{tech_innovators.name}'.")
    else:
        print("Magazine 'Tech Innovators' not found.")

    mags_with_multiple_authors = Magazine.with_multiple_authors()
    print("\nMagazines with multiple authors:")
    for mag in mags_with_multiple_authors:
        print(f"- {mag.name}")

    counts = Magazine.article_counts()
    print("\nArticle counts per magazine:")
    for name, count in counts.items():
        print(f"- {name}: {count} articles")