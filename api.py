from flask_restful import Resource, Api
from flask import request
from fastapi import FastAPI
from models import *

api = Api()


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
        books = Book.query.all()
        return [{
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "reviews": [r.text for r in book.reviews]
        } for book in books], 200

    def post(self):
        title = request.json.get('title')
        author = request.json.get('author')
        if Book.query.filter_by(title=title).first():
            return {"message": "Book already exists"}, 409
        new_book = Book(title=title, author=author)
        db.session.add(new_book)
        db.session.commit()
        return {"message": "Book added successfully"}, 201


class BookDetailAPI(Resource):
   
    def put(self, id):
        book = Book.query.get(id)
        if not book:
            return {"message": "Book not found"}, 404
        book.title = request.json.get("title", book.title)
        book.author = request.json.get("author", book.author)
        db.session.commit()
        return {"message": "Book updated successfully"}, 200

    def delete(self, id):
        book = Book.query.get(id)
        if not book:
            return {"message": "Book not found"}, 404
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted successfully"}, 200

class ReviewListAPI(Resource):
    def get(self, id):
        book = Book.query.get_or_404(id)
        return [
            {"id": r.id, "text": r.text}
            for r in book.reviews
        ], 200

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
api.add_resource(BookDetailAPI,  "/books/<int:id>")
api.add_resource(ReviewListAPI,  "/books/<int:id>/reviews")

# api.add_resource(BookListAPI, "/books")  # GET & POST
# api.add_resource(BookDetailAPI, "/books/<int:id>")  # PUT & DELETE




app = FastAPI()  # FastAPI auto‑generates /docs for you

@app.get("/books")
def list_books():
    return [{"id": 1, "title": "Dune"}]
