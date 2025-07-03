# tests/test_cache.py
from api import cache

def test_books_cache_miss(client):
    # Ensure cache is empty
    cache.flushall()

    # Add a book directly
    client.post("/books", json={"title": "CacheBook", "author": "Cached"})

    # First GET should fall back to DB
    response = client.get("/books")
    assert response.status_code == 200
    books = response.get_json()
    assert any(book["title"] == "CacheBook" for book in books)
