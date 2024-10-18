from flask_restx import reqparse

user_reset_password_parser = reqparse.RequestParser()
user_reset_password_parser.add_argument(
    "old_password",
    type=str,
    location="json",
    required=True,
    nullable=False,
    trim=True,
)
user_reset_password_parser.add_argument(
    "new_password",
    type=str,
    location="json",
    required=True,
    nullable=False,
    trim=True,
)
user_reset_password_parser.add_argument(
    "confirmed_password",
    type=str,
    location="json",
    required=True,
    nullable=False,
    trim=True,
)