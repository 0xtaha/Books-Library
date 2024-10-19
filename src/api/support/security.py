import os, re
from functools import wraps
from flask import abort, request , current_app
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import PyJWTError
import hmac , hashlib, base64
from html import escape
from passlib.context import CryptContext
from .exceptions import *
from ...models_services.user_model_services import UserModelServices as User
from ...connections_handeller import RedisConnector

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


authorizations = {
    "bearer_token": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": (
            "Enter the jwt token with the `Bearer ` prefix, e.g. 'Bearer"
            " abcde12345'."
        ),
    }
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

def hash_password(password):
    if use_double_hash():
        password = get_hmac(password).decode("ascii")
    return password_context_manager.hash(password, "bcrypt")



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

def get_identity():
    identity = get_jwt_identity()
    if not isinstance(identity, dict):
        abort(422, "Invalid JWT token")
    if not identity.get("user_id", False):
        abort(401, "Invalid JWT token, please re-authenticate")

    return identity["user_id"]


def valid_jwt_required():
    """check JWT validity and signature"""

    def main_decorator(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if 'Authorization' not in request.headers:
                abort(401,"Authorization header is missing")
            try:
                verify_jwt_in_request()
            except PyJWTError as e:
                abort(401,"access token provided is invalid or expired")
            except NoAuthorizationError as e:
                abort(401, 'Authorization Not found')

            identity = get_jwt_identity()
            if not isinstance(identity, dict):
                abort(422, "Invalid JWT token")
            if not identity.get("user_id", False):
                abort(401, "Invalid JWT token, please re-authenticate")

            user_id = identity["user_id"]
            try:
                user = User.get_user_by_id(user_id)
                if not user or not get_jwt_session(user_id):
                    abort(401, "Invalid JWT token, please re-authenticate")
                if not user.active:
                    abort(401, "User account is disabled")
                return f(*args, **kwargs)
            except NotFound as e:
                current_app.logger.warning(
                    "Unauthorized access by unknown user caused the following"
                    f" exception  exception: {e}"
                )
                abort(401, "Unauthorized")
            except DBError as e:
                current_app.logger.error(
                    "valid_jwt_required caused the following exception "
                    f" exception: {e}"
                )
                abort(500, "Internal server error")

        return decorator

    return main_decorator

 
def get_user_by_credentials(email, password):

    user = User.get_by_mail(email)
    if not user:
        return None
    password_is_valid = verify_password(password, user.password)
    if password_is_valid:
        return user
    else:
        return False


def is_email_RFC5322(email):
    """validate email input according to RFC5322 standard"""
    regex = re.compile(
        r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~"
        r" \t]|(\\[\t -~]))+\")"
        r"@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
    )
    return re.fullmatch(regex, email)

def get_jwt_session(user_id):
    redis_connector = RedisConnector()
    client = redis_connector.rdb
    namespace = "USER_ACTIVE_SESSIONS_NAMESPACE"
    key = str(user_id)
    qualified_key = f"{namespace}:{key}"
    jwt = client.get(qualified_key)
    return jwt.decode() if jwt else None


def sanitize_xss(input_string):
    """
    Sanitize the input string to remove potential XSS scripts.
    
    This function performs the following actions:
    1. Escapes HTML special characters
    2. Removes JavaScript events
    3. Removes common XSS vector tags
    4. Removes inline CSS
    5. Removes data URIs
    
    Args:
    input_string (str): The input string to sanitize

    Returns:
    str: The sanitized string
    """
    if not isinstance(input_string, str):
        return ""

    # Step 1: Escape HTML special characters
    sanitized = escape(input_string)
    
    # Step 2: Remove JavaScript events
    sanitized = re.sub(r'on\w+\s*=\s*".*?"', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"on\w+\s*=\s*'.*?'", "", sanitized, flags=re.IGNORECASE)
    
    # Step 3: Remove common XSS vector tags
    sanitized = re.sub(r'<(script|style|iframe|object|embed|base).*?>.*?</\1>', '', sanitized, flags=re.IGNORECASE|re.DOTALL)
    
    # Step 4: Remove inline CSS
    sanitized = re.sub(r'style\s*=\s*".*?"', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"style\s*=\s*'.*?'", "", sanitized, flags=re.IGNORECASE)
    
    # Step 5: Remove data URIs
    sanitized = re.sub(r'data:\s*\w+/\w+;base64,\S+', '', sanitized, flags=re.IGNORECASE)
    
    return sanitized