import datetime
from flask import request
from ....connections_handeller import RedisConnector
from flask_restx import abort
from flask_jwt_extended import create_access_token
from ...support.security import get_identity, hash_password, is_email_RFC5322 , get_user_by_credentials
from ...support import exceptions
from ....models_services.user_model_services import UserModelServices as User
from ....default_config import DefaultConfig

class UserService:

    redis_connector = RedisConnector()

    @classmethod
    def register_new_user(cls, args):
        if cls.check_user_exist_by_email(args['email']):
            abort(400, 'User already exist')
        if not is_email_RFC5322(args["email"]):
            abort(400,"Invalid email format")

        user_info = User.create_new_user(
            user_info=args,
            request_ip_address=UserService.get_request_ip(),
            hashed_password=hash_password(args['password'])
        )
        return user_info



    @classmethod
    def check_user_exist_by_email(cls, email):
        return User.get_by_mail(email)

    @classmethod
    def get_request_ip(cls):
        if request.environ.get("HTTP_X_FORWARDED_FOR") is None:
            request_ip = request.environ["REMOTE_ADDR"]
        else:
            request_ip = request.environ["HTTP_X_FORWARDED_FOR"]
        return request_ip


    @classmethod
    def log_in_user(cls, user_info):
        """get fresh jwt token for an existing user"""
        if not is_email_RFC5322(user_info["email"]):
            abort(400,"Invalid email format")
        user = get_user_by_credentials(
            user_info["email"], user_info["password"]
        )
        if user is None:
            abort(400, "User Doesn't Exist")
        if not user :
            abort(401, 'Invalide Credentials')
        if not user:
            abort(404,"User is not found")

        request_ip_address = UserService.get_request_ip()
        user.update_after_login(request_ip_address)

        # check if the user has an active session
        jwt_token = cls.get_jwt_session(user)

        # create a new session
        if not jwt_token:
            jwt_token = cls.create_new_jwt_session(user)

        return user.id, jwt_token

    @classmethod
    def get_jwt_session(cls, user_id):
        client = cls.redis_connector.rdb
        namespace = "USER_ACTIVE_SESSIONS_NAMESPACE"
        key = str(user_id)
        qualified_key = f"{namespace}:{key}"
        jwt = client.get(qualified_key)
        return jwt.decode() if jwt else None

    @classmethod
    def create_new_jwt_session(cls, user):
        client = cls.redis_connector.rdb
        expire_after = datetime.timedelta(
            hours= DefaultConfig.JWT_EXPIRE['hours'],
            minutes= DefaultConfig.JWT_EXPIRE['mins'],
            seconds= DefaultConfig.JWT_EXPIRE['sec'],
        )

        namespace = "USER_ACTIVE_SESSIONS_NAMESPACE"

        jwt_token = create_access_token(
            identity={"user_id": user.id}, expires_delta=expire_after
        )

        key = str(user.id)
        value = jwt_token

        qualified_key = f"{namespace}:{key}"
        client.setex(qualified_key, expire_after, value)

        return jwt_token

    @classmethod
    def logout_user_session(cls, user_id):
        # Todo : change to reading the configration for app
        client = cls.redis_connector.rdb
        namespace = "USER_ACTIVE_SESSIONS_NAMESPACE"
        key = str(user_id)
        qualified_key = f"{namespace}:{key}"

        client.delete(qualified_key)

    @classmethod
    def log_out_user(cls, jwt_token):
        """blacklist user's fresh jwt token"""
        user_id = jwt_token["sub"]["user_id"]
        cls.logout_user_session(user_id)

    @classmethod
    def get_all_users(cls, role_filter=None, paginate_by=None, page=1):
        query = User.select().order_by(User.email.asc())
        total_users_count = query.count()
        if paginate_by:
            query = query.paginate(page, paginate_by)
        return total_users_count, [user.serialize() for user in query if user is not None]
    

    @classmethod
    def delete_user(cls, user_id):
        """delete user roles"""
        user = User.get_user_by_id(user_id)

        if not user:
            raise exceptions.NotFound(
                f"DELETE_USER_PRIVILEGES, user_id={user_id}, reason= USER_DOES_NOT_EXIST ",
            )
        
        requester_user_roles = cls.load_user_roles(get_identity())
        user_roles = cls.load_user_roles(user.id)

        if not cls.check_the_requester_roles_to_manage_user(user_roles, requester_user_roles):
            raise exceptions.UnauthorizedAccess
        
        status = user.delete_user()
        if not status:
            raise exceptions.ParameterError
        return True
        
    @classmethod
    def check_jwt_status(cls, jwt_token):
        user_id = jwt_token["sub"]["user_id"]
        return cls.get_jwt_session(user_id)

    @classmethod
    def get_user_count(cls):
        return User.select().count()
    
    @classmethod
    def get_user_info(cls, user_id):
        return User.get_user_by_id(user_id).serialize()
        