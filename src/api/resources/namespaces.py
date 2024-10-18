from flask_restx import Namespace

NAMESPACES = {
    "User": Namespace("users", description="endpoint for operations related to users"),
    "Book" : Namespace("books", description="endpoint for operations related to books and reviews")
}
