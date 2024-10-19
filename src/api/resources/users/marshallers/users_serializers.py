from flask_restx import fields

from ...namespaces import NAMESPACES

user_ns = NAMESPACES["User"]


user_fields = {}
user_fields["id"] = fields.Integer()
user_fields["email"] = fields.String()
user_fields["last_login_at"] = fields.DateTime()
user_fields["last_login_ip"] = fields.String()
user_fields["login_count"] = fields.Integer()

user_fields_model = user_ns.model("userFieldsModel", user_fields)

user_standard_serializer = user_ns.model(
    "UserStandard",
    {
        "message": fields.String(),
        "status": fields.String(),
    },
)

user_creation_serializer = user_ns.model(
    "UserCreation",{
        "id": fields.Integer(),
        "email":fields.String(),
    }
)


user_login_serializer = user_ns.model(
    "UserLogin",
    {
        "message": fields.String(),
        "status": fields.String(),
        "id": fields.String(),
        "access_token": fields.String(),
    },
)
