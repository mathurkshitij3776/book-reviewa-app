# tests/test_books.py
def test_add_book(client):
    response = client.post("/books", json={"title": "TestBook", "author": "AuthorX"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "TestBook"

def test_get_books(client):
    # Add book first
    client.post("/books", json={"title": "ReadMe", "author": "AuthorA"})
    
    # Now GET
    response = client.get("/books")
    assert response.status_code == 200
    books = response.get_json()
    assert isinstance(books, list)
    assert books[0]["title"] == "ReadMe"

def test_add_review(client):
    # First add book
    post_book = client.post("/books", json={"title": "ReviewBook", "author": "TestAuthor"})
    book_id = post_book.get_json()["id"]

    # Now post review
    response = client.post(f"/books/{book_id}/reviews", json={"text": "Nice one!"})
    assert response.status_code == 201
    assert response.get_json()["text"] == "Nice one!"
