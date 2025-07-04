# # schema.py  (put in project root)
# import graphene
# from models import db, Book, Review

# # 1️⃣  GraphQL types (hand‑written — no graphene_sqlalchemy needed)
# class ReviewType(graphene.ObjectType):
#     id    = graphene.Int()
#     text  = graphene.String()

# class BookType(graphene.ObjectType):
#     id      = graphene.Int()
#     title   = graphene.String()
#     author  = graphene.String()
#     reviews = graphene.List(ReviewType)

#     # resolve nested reviews
#     def resolve_reviews(parent, info):
#         return parent.reviews

# # 2️⃣  Queries
# class Query(graphene.ObjectType):
#     all_books = graphene.List(BookType)
#     book      = graphene.Field(BookType, id=graphene.Int(required=True))

#     def resolve_all_books(root, info):
#         return Book.query.all()

#     def resolve_book(root, info, id):
#         return Book.query.get(id)

# # 3️⃣  Mutations
# class AddReview(graphene.Mutation):
#     class Arguments:
#         book_id = graphene.Int(required=True)
#         text    = graphene.String(required=True)

#     ok     = graphene.Boolean()
#     review = graphene.Field(lambda: ReviewType)

#     def mutate(root, info, book_id, text):
#         book = Book.query.get(book_id)
#         if not book:
#             raise Exception("Book not found")

#         review = Review(text=text, book_id=book_id)
#         db.session.add(review)
#         db.session.commit()
#         return AddReview(ok=True, review=review)

# class Mutation(graphene.ObjectType):
#     add_review = AddReview.Field()

# # 4️⃣  Assemble schema
# schema = graphene.Schema(query=Query, mutation=Mutation)
