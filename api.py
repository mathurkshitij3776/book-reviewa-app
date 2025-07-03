from flask_restful import Resource, Api
from flask import request, current_app
from models import *
import json
import fakeredis
api = Api()

cache = fakeredis.FakeRedis()

# class ShowAPi(Resource):
#     # GET /api/Books returns all Books with their chapters
    
#     def get(self):
#         books = Book.query.all() 
#         b_list = []
#         for book in books:
#             b_list.append({"id": book.id, "title": book.title, "author": book.author, "reviews":[review.txt for review in book.reviews]})
#         return (b_list), 200
    

#     def post(self):
#         title = request.json.get('title')
#         description = request.json.get('description')
#         Book = Book.query.filter_by(title = title).first()
#         if not Book:
#             new_Book=  Book(title = title, description = description)
#             db.session.add(new_Book)
#             db.session.commit()
#             return {"message":"Book added succesfully"}, 201
#         return {"message":"Book already exist"}

#     def post(self, id):
#         review =request.json.get('text')
#         existing_book = Book.query.filter_by(id = id).first()
#         if existing_book:
#             if review:
#                 new_review = Review(text = review, book_id = id)
#                 db.session.add(new_review)
#                 db.session.commit()
#                 return {"message": "review added successfully"} ,200
#         return {"message":"Book does not exist. First add then do edit"}, 404
    
#     def get(self, id):
#         book = Review.query.filter_by(book_id = id).first() 
#         reviews = book.reviews
#         r_list = []
#         for review in reviews:
#             r_list.append({"id": book.id, "title": book.title, "author": book.author, "reviews":[review.txt for review in book.reviews]})
#         return (r_list), 200
    
        
    
# api.add_resource(ShowAPi, "/Books", "/add_Book", "/Books/<int:id>/reviews", "/Books/<int:id>/reviews")
class BookListAPI(Resource):
    def get(self):

        try:
            raw = cache.get("all_books")           # attempt to fetch
            if raw:
                books = json.loads(raw)           # parse JSON bytes
                current_app.logger.info("Served /books from cache")
                return books, 200                 # return cached data
        except Exception as e:
            current_app.logger.warning(f"Cache read failed ({e}) — falling back to DB")
        
        books = Book.query.all()
        return [{
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "reviews": [r.text for r in book.reviews]
        } for book in books], 200
        
     

    def post(self):
  # Validate input
        data = request.get_json() or {}
        title = data.get("title")
        author = data.get("author")
        if not title or not author:
            return {"message": "Both title and author are required"}, 400

        # Check for duplicates
        if Book.query.filter_by(title=title).first():
            return {"message": "Book already exists"}, 409

        # Create and save
        new_book = Book(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()

        # ─── Invalidate cache so next GET is fresh ────────────────
        try:
            cache.delete("all_books")
            current_app.logger.info("Invalidated /books cache after POST")
        except Exception as e:
            current_app.logger.warning(f"Cache delete failed ({e})")

        return {"id": new_book.id, "title": new_book.title}, 201
        # title = request.json.get('title')
        # author = request.json.get('author')
        # if Book.query.filter_by(title=title).first():
        #     return {"message": "Book already exists"}, 409
        # new_book = Book(title=title, author=author)
        # db.session.add(new_book)
        # db.session.commit()
        # return {"message": "Book added successfully"}, 201
        


# class BookDetailAPI(Resource):
   
#     def put(self, id):
#         book = Book.query.get(id)
#         if not book:
#             return {"message": "Book not found"}, 404
#         book.title = request.json.get("title", book.title)
#         book.author = request.json.get("author", book.author)
#         db.session.commit()
#         return {"message": "Book updated successfully"}, 200

#     def delete(self, id):
#         book = Book.query.get(id)
#         if not book:
#             return {"message": "Book not found"}, 404
#         db.session.delete(book)
#         db.session.commit()
#         return {"message": "Book deleted successfully"}, 200

class ReviewListAPI(Resource):
    def get(self, id):
        book = Book.query.filter_by(id = id).first()
        if book:    
            reviews = book.reviews
            if reviews:
                return [
                    {"id": r.id, "text": r.text}
                    for r in reviews
                ], 200
            else:
                return {"message": "no reviews"}
        return {"message": "book not found "}   
    
    
    def post(self, id):
        book = Book.query.get_or_404(id)
        data = request.get_json()
        if not data.get("text"):
            return {"message": "Review text required"}, 400
        review = Review(text=data["text"], book_id=book.id)
        db.session.add(review); db.session.commit()
        return {"id": review.id, "text": review.text}, 201
    
# Register resources
api.add_resource(BookListAPI,    "/books")
# api.add_resource(BookDetailAPI,  "/books/<int:id>")
api.add_resource(ReviewListAPI,  "/books/<int:id>/reviews")

# api.add_resource(BookListAPI, "/books")  # GET & POST
# api.add_resource(BookDetailAPI, "/books/<int:id>")  # PUT & DELETE





