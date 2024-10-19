from flask_restx import reqparse

get_book_parser = reqparse.RequestParser()

get_book_parser.add_argument(
    "book_id",
    type=int,
    location='args',
    help="book identifier",
    required=True,
    nullable=False,
)
#############################
get_books_parser = reqparse.RequestParser()

get_books_parser.add_argument(
    "page_size",
    type=int,
    location='args',
    help="response page number",
    required=False,
    nullable=False,
    default=20,
)

get_books_parser.add_argument(
    "page_number",
    type=int,
    location='args',
    help="number of items per page, max 10000",
    required=True,
    nullable=False,
)

###############################

post_review_parser = reqparse.RequestParser()

post_review_parser.add_argument(
    "book_id",
    type=int,
    location='args',
    help="book identifier",
    required=True,
    nullable=False,
)

post_review_parser.add_argument(
    "desc",
    type=str,
    location='json',
    help="book review",
    required=True,
    nullable=False,
)