from flask_restx import reqparse

user_get_parser = reqparse.RequestParser()

user_get_parser.add_argument(
    "page",
    type=int,
    location='args',
    help="response page number",
    required=False,
    nullable=False,
    default=1,
)

user_get_parser.add_argument(
    "paginate_by",
    type=int,
    location='args',
    help="number of items per page, max 10000",
    required=False,
    nullable=False,
)