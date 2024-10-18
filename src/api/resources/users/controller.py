from math import ceil
from flask import request
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_restx import Resource, abort
from jwt import ExpiredSignatureError
from ...support import exceptions
from ..namespaces import NAMESPACES
from .marshallers.users_serializers import (
    user_login_serializer,
    user_fields_model,
    user_standard_serializer,
    user_retrieve_serializer,
    user_creation_serializer
)
from .parsers.user_reset_password import user_reset_password_parser
from .parsers.user_login_parser import user_login_parser
from .parsers.user_sign_up_parser import user_signup_parser
from .parsers.user_get_parser import user_get_parser
from .service.user_service import UserService
from ...support.security import valid_jwt_required

user_ns = NAMESPACES["User"]

@user_ns.route("/info")
class RetriveCurrentUserInfo(Resource):
    @user_ns.marshal_with(user_fields_model)
    @user_ns.response(200, "Success")
    @user_ns.response(500, "Internal Server Error")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(404, "Not Found")
    @user_ns.response(400, "Bad request")
    @valid_jwt_required()
    def get(self):
        try:
            verify_jwt_in_request()
            jwt_identity = get_jwt_identity()
            if not jwt_identity.get("user_id", False):
                raise exceptions.BadJWTSignature(
                    f"LOAD_USER_FROM_REQUEST {jwt_identity} reason= BAD_PAYLOAD",
                )

            user_id = jwt_identity["user_id"]
            return UserService.get_user_info(user_id)
        except (ExpiredSignatureError, JWTExtendedException):
            http_response = {"message": "disconnected", "status": "fail"}
            return http_response


@user_ns.route("/status")
class UserStatus(Resource):
    """User endpoint to get the status of JWT"""
    @user_ns.marshal_with(user_standard_serializer)
    @user_ns.response(200, "Success")
    @user_ns.response(400, "Bad request")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(404, "Not found")
    @user_ns.response(422, "Bad JWT signature")
    @user_ns.response(500, "Internal Server Error")
    @valid_jwt_required()

    @user_ns.doc(security=[])
    def get(self):
        """check if jwt session key is still active"""
        try:
            verify_jwt_in_request()
        except (ExpiredSignatureError, JWTExtendedException):
            http_response = {"message": "disconnected", "status": "fail"}
            return http_response
        jwt_token = get_jwt()
        jwt_is_valid = UserService.check_jwt_status(jwt_token)
        if jwt_is_valid:
            http_response = {
                "message": "connected",
                "status": "success",
            }
        else:
            http_response = {"message": "disconnected", "status": "fail"}
        return http_response


@user_ns.route("/login")
class UserLogin(Resource):
    """Endpoint for user authentication"""

    @user_ns.marshal_with(user_login_serializer)
    @user_ns.expect(user_login_parser, validate=True)
    @user_ns.response(200, "Successfully connected")
    @user_ns.response(400, "Bad request")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(500, "Internal Server Error")
    @user_ns.doc(security=[])
    def post(self):
        """Login user to get a valid JWT access token"""
        args = user_login_parser.parse_args(strict=True)

        try:
            user_id, jwt_token = UserService.log_in_user(args)
            http_response = {
                "status": "success",
                "message": "Successfully connected.",
                "id": user_id,
                "access_token": jwt_token,
            }
            return http_response

        except exceptions.ParameterError as e:
            user_ns.logger.warning(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(400, "Bad inputs")
        except exceptions.NotFound as e:
            user_ns.logger.warning(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(401, "Unauthorized")
        except exceptions.DBError as e:
            user_ns.logger.error(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(500, "Internal Server Error")


@user_ns.route("/logout")
class UserLogout(Resource):
    """User endpoint to log out a user by blacklisting his JWT"""

    @user_ns.marshal_with(user_standard_serializer)
    @user_ns.response(200, "Success")
    @user_ns.response(400, "Invalid JWT Access Token")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(422, "Bad JWT signature")
    @user_ns.response(500, "Internal Server Error")
    @valid_jwt_required()
    def get(self):
        """Logout user"""
        try:
            jwt = get_jwt()

            UserService.log_out_user(jwt)
            http_response = {
                "status": "success",
                "message": "Token successfully blacklisted",
            }
            return http_response
        except exceptions.AlreadyExists:
            http_response = {
                "status": "success",
                "message": "JWT token already blacklisted",
            }
            return http_response
        except exceptions.DBError as e:
            user_ns.logger.error(
                "The following Exception occurred on this endpoint:"
                f" '{request.url}' : {e}"
            )
            abort(500, "Internal Server Error")


@user_ns.route("/signup")
class UserSignUp(Resource):
    """User endpoint to create new user"""

    @user_ns.marshal_with(user_creation_serializer)
    @user_ns.expect(user_signup_parser, validate=True)
    @user_ns.response(201, "Successfully created")
    @user_ns.response(401, "Unauthorized")
    @user_ns.response(409, "Already exists")
    @user_ns.response(500, "Internal Server Error")
    def post(self):
        args = user_signup_parser.parse_args(strict=True)
        return UserService.register_new_user(args), 201
       


    
