from flask_restx import reqparse

user_signup_parser = reqparse.RequestParser()

user_signup_parser.add_argument(
    "email",
    type=str,
    location="json",
    required=True,
    nullable=False,
    trim=True,
)

user_signup_parser.add_argument(
    "password",
    type=str,
    location="json",
    required=True,
    nullable=False,
    trim=True,
)

user_signup_parser.add_argument(
    "firstname",
    type=str,
    location="json",
    default=None,
    required=False,
    trim=True,
)

user_signup_parser.add_argument(
    "lastname",
    type=str,
    location="json",
    default=None,
    required=False,
    trim=True,
)

