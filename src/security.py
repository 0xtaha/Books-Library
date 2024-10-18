import os
from functools import wraps
from logging import getLogger
from flask import abort, request , current_app
import hmac , hashlib, base64
from passlib.context import CryptContext
from .exceptions import DBError


"""######### Flask-security Password hashing and verify schema #########"""

PASSWORD_HASH = "bcrypt"
PASSWORD_SCHEMES = [
    "bcrypt",
    "des_crypt",
    "pbkdf2_sha256",
    "pbkdf2_sha512",
    "sha256_crypt",
    "sha512_crypt",
    "plaintext",
]
DEPRECATED_PASSWORD_SCHEMES = ["auto"]


api_key_authorizations = {
    "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Enter the API Key in the header as Authorization",
    },
}


def load_client_id(path : str):
    """
    Load Client ID from headers in order to identify the correct API Key
    """

    client_id = path.split('/')[-1]
    return client_id


def load_api_key(headers):
    """load api key from Authorization field
    if it exists and check for api key validity
    """
    if 'Authorization' not in headers:
        return None
    api_key = headers["Authorization"]
    return api_key



def get_hmac(password):
    """Returns a Base64 encoded HMAC+SHA512 of the password signed with
    the salt specified by ``SECURITY_PASSWORD_SALT``"""
    salt = os.environ.get("SECURITY_PASSWORD_SALT")
    if salt is None:
        raise RuntimeError(
            "The configuration value `SECURITY_PASSWORD_SALT` must "
            "not be None "
        )
    h = hmac.new(
        salt.encode("utf-8"), password.encode("utf-8"), hashlib.sha512
    )
    return base64.b64encode(h.digest())

password_context_manager = CryptContext(
    schemes=PASSWORD_SCHEMES,
    default="bcrypt",
    deprecated=DEPRECATED_PASSWORD_SCHEMES,
)


def verify_password(input_password, existing_password):
    if use_double_hash(existing_password):
        input_password = get_hmac(input_password)
    return password_context_manager.verify(input_password, existing_password)

def use_double_hash(password_hash=None):
    """Return a bool indicating if a password should be hashed twice."""
    if password_hash is None:
        is_plaintext = PASSWORD_HASH == "plaintext"
    else:
        is_plaintext = (
            password_context_manager.identify(password_hash) == "plaintext"
        )

    return not is_plaintext