
from flask_restful import Resource, Api
from flask import request, current_app, jsonify
from models import db, Book, Review
import json, fakeredis
#from schema import schema
api = Api()                       # created once, attached later in create_app()
cache = fakeredis.FakeRedis()     # fake Redis cache for local dev & tests
#app = current_app()
from flasgger import swag_from
class BookListAPI(Resource):
    def get(self):
        """
        Get all books with their reviews
        ---
        responses:
          200:
            description: List of books
        """
    
        try:                                  # cache‑first
            raw = cache.get("all_books")
            if raw:
                current_app.logger.info("Served /books from cache")
                return json.loads(raw), 200
        except Exception as e:
            current_app.logger.warning(f"Cache read failed ({e}); falling back to DB")

        books = Book.query.all()
        result = [
            {
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "reviews": [r.text for r in b.reviews],
            }
            for b in books
        ]

        # store in cache
        try:
            cache.set("all_books", json.dumps(result))
        except Exception as e:
            current_app.logger.warning(f"Cache write failed ({e})")

        return result, 200

    def post(self):
        """
        Add a new book
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required: [title, author]
              properties:
                title:  {type: string}
                author: {type: string}
        responses:
          201: {description: Book created}
          400: {description: Missing title/author}
          409: {description: Duplicate title}
        """
        data = request.get_json() or {}
        title = data.get("title")
        author = data.get("author")

        if not title:
            return {"message": "Title is required"}, 400
        if not author:
            return {"message": "Author is required"}, 400

        if Book.query.filter_by(title=title).first():
            return {"message": "Book already exists"}, 409

        book = Book(title=title, author=author)
        db.session.add(book)
        db.session.commit()

        cache.delete("all_books")   # invalidate list cache
        return {"id": book.id, "title": book.title}, 201


class BookDetailAPI(Resource):
    def put(self, id):
        book = Book.query.get(id)
        if not book:
            return {"message": "Book not found"}, 404
        book.title  = request.json.get("title",  book.title)
        book.author = request.json.get("author", book.author)
        db.session.commit()
        cache.delete("all_books")
        return {"message": "Book updated"}, 200

    def delete(self, id):
        book = Book.query.get(id)
        if not book:
            return {"message": "Book not found"}, 404
        db.session.delete(book)
        db.session.commit()
        cache.delete("all_books")
        return {"message": "Book deleted"}, 200


class ReviewListAPI(Resource):
    def get(self, id):
        book = Book.query.get(id)
        if not book:
            return {"message": "Book not found"}, 404
        if not book.reviews:
            return {"message": "No reviews"}, 200
        return [{"id": r.id, "text": r.text} for r in book.reviews], 200

    def post(self, id):
        book = Book.query.get_or_404(id)
        text = request.json.get("text")
        if not text:
            return {"message": "Review text required"}, 400
        review = Review(text=text, book_id=book.id)
        db.session.add(review)
        db.session.commit()
        cache.delete("all_books")
        return {"id": review.id, "text": text}, 201







# Register every route ONCE
api.add_resource(BookListAPI,   "/books")
api.add_resource(BookDetailAPI, "/books/<int:id>")
api.add_resource(ReviewListAPI, "/books/<int:id>/reviews")



