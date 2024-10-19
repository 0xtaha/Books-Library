from flask_restx import fields

from ..namespaces import NAMESPACES

book_ns = NAMESPACES["Book"]


book = {}
book["id"] = fields.Integer()
book["title"] = fields.String()


book_model = book_ns.model("BookFieldsModel", {
    "id" : fields.Integer(),
    "title" : fields.String()
})

book_content_model = book_ns.model('book_content_model',{
    "id" : fields.Integer(),
    "title" : fields.String(),
    "content" : fields.String()
})


books_response_model = book_ns.model('BooksResponse', {
    'total_count': fields.Integer(required=True, description='Total number of books'),
    'books': fields.List(fields.Nested(book_model), required=True, description='List of books')
})

##############
review_user_model = book_ns.model('User', {
    'email': fields.String(required=True, description='User email')
})

# Review model
review_model = book_ns.model('Review', {
    'id': fields.Integer(required=True, description='Review identifier'),
    'user': fields.Nested(review_user_model, required=True, description='User who wrote the review'),
    'desc': fields.String(required=True, description='Review description')
})

# Book model with nested reviews
book_review_model = book_ns.model('Book', {
    'id': fields.Integer(required=True, description='Book identifier'),
    'title': fields.String(required=True, description='Book title'),
    'reviews': fields.List(fields.Nested(review_model), required=True, description='List of reviews')
})