from ..models import User
from peewee import PeeweeException , fn
from ..api.support.exceptions import DBError, NotFound, AlreadyExists
from flask import current_app
from datetime import datetime

class UserModelServices:

    @classmethod
    def create_new_user(cls, user_info, request_ip_address, hashed_password, active = True):
        """create new user instance"""
        
        user_obj = User.create(
            email=user_info["email"],
            password= hashed_password,
            active=active,
            firstname=user_info["firstname"],
            lastname=user_info["lastname"],
            last_login_at= datetime.now(),
            last_login_ip=request_ip_address,
        )

        return user_obj.serialize()
        

    

    @classmethod
    def get_user_by_id(cls, id):
        try:
           return User.get_or_none(User.id == id)

        except PeeweeException as e:
            current_app.logger.error(
                "Database error occurred in 'get_user_id' method : {}".format(e)
            )
            raise DBError
        

    @classmethod
    def get_by_mail(cls, email) :
        return User.get_or_none(User.email == email)
