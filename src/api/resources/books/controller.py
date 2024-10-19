from flask import request
from flask_restx import Resource, abort
from flask_jwt_extended import verify_jwt_in_request
from ...support import exceptions
from ..namespaces import NAMESPACES
from ...support.security import valid_jwt_required, get_identity, sanitize_input
from .marshallers import book_model, book_content_model, book_review_model, books_response_model
from .parsers import get_book_parser, get_books_parser, post_review_parser
from .services import BookServices

book_ns = NAMESPACES["Book"]

@book_ns.route("")
class RetriveAllBooks(Resource):
    @book_ns.expect(get_books_parser)
    @book_ns.marshal_with(books_response_model)
    @book_ns.response(200, "Success")
    @book_ns.response(500, "Internal Server Error")
    @book_ns.response(401, "Unauthorized")
    @book_ns.response(404, "Not Found")
    @book_ns.response(400, "Bad request")
    @valid_jwt_required()
    def get(self):
        try:
            args = get_books_parser.parse_args()
            return BookServices.get_list(args), 200
        except exceptions.DBError as e:
            book_ns.logger.error(f"error on {request.url}, {e}")
            abort(500, 'Internal server Error')

@book_ns.route('/content')
class RetriveBookContent(Resource):
    @book_ns.expect(get_book_parser)
    @book_ns.marshal_with(book_content_model)
    @book_ns.response(200, "Success")
    @book_ns.response(500, "Internal Server Error")
    @book_ns.response(401, "Unauthorized")
    @book_ns.response(404, "Not Found")
    @book_ns.response(400, "Bad request")
    @valid_jwt_required()
    def get(self):
        try:
            args = get_book_parser.parse_args()
            return BookServices.get_book_content(book_id=args['book_id']), 200
        except exceptions.DBError as e:
            book_ns.logger.error(f"error on {request.url}, {e}")
            abort(500, 'Internal server Error')


@book_ns.route('/reviews')
class RetriveBookReviews(Resource):
    @book_ns.expect(get_book_parser)
    @book_ns.marshal_with(book_review_model)
    @book_ns.response(200, "Success")
    @book_ns.response(500, "Internal Server Error")
    @book_ns.response(401, "Unauthorized")
    @book_ns.response(404, "Not Found")
    @book_ns.response(400, "Bad request")
    @valid_jwt_required()
    def get(self):
        try:
            args = get_book_parser.parse_args()
            return BookServices.get_book_and_reviews(book_id=args['book_id']), 200
        except exceptions.DBError as e:
            book_ns.logger.error(f"error on {request.url}, {e}")
            abort(500, 'Internal server Error')

    @book_ns.expect(post_review_parser)
    @book_ns.response(201, "Success")
    @book_ns.response(500, "Internal Server Error")
    @book_ns.response(401, "Unauthorized")
    @book_ns.response(404, "Not Found")
    @book_ns.response(400, "Bad request")
    def post(self):
        try:
            verify_jwt_in_request()
            args = post_review_parser.parse_args()
            desc = sanitize_input(args['desc'])
            args = post_review_parser.parse_args()
            return BookServices.create_review_on_book(
                book_id=args['book_id'],
                desc=desc,
                user_id= get_identity()
                ), 201
        except ValueError as e:
            book_ns.logger.error(f"error on {request.url}, {e}")
            abort(400, 'Invalid Please check you request')
        except exceptions.DBError as e:
            book_ns.logger.error(f"error on {request.url}, {e}")
            abort(500, 'Internal server Error')