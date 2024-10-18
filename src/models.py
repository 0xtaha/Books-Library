import peewee
from .db_handeller import DBConnector

db_connector = DBConnector()
class BaseModel(peewee.Model):
    class Meta:
        database = db_connector.pg_db


class User(BaseModel):
    id = peewee.AutoField()
    password = peewee.CharField()
    email = peewee.CharField(unique=True)
    active = peewee.BooleanField(default=False)
    last_login_at = peewee.DateTimeField(null=True)
    last_login_ip = peewee.CharField(null=True)
    login_count = peewee.IntegerField(default=0)

    # Apikey has been removed from users

    def serialize(self):
        content = {
            field: getattr(self, field)
            for field in (
                "id",
                "email",
                "active",
                "last_login_at",
                "last_login_ip",
                "login_count",
            )
        }
        return content
