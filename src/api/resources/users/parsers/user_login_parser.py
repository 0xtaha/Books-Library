from flask_restx import reqparse

user_login_parser = reqparse.RequestParser()

user_login_parser.add_argument(
    "email",
    type=str,
    location="json",
    required=True,
    nullable=False,
)
user_login_parser.add_argument(
    "password",
    type=str,
    location="json",
    required=True,
    nullable=False,
)
