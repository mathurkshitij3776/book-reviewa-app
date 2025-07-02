from database import db


class Book(db.Model):
    id     = db.Column(db.Integer, primary_key=True)
    title  = db.Column(db.String(200), unique=True, nullable=False)
    author = db.Column(db.String(200), nullable=False)
    reviews = db.relationship("Review", back_populates="book", lazy="select")

class Review(db.Model):
    id      = db.Column(db.Integer, primary_key=True, autoincrement= True)
    text    = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False, index=True)
    book = db.relationship("Book", back_populates="reviews")

