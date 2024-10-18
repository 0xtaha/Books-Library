import peewee
from datetime import datetime
from .connections_handeller import DBConnector

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
    login_count = peewee.IntegerField(default=1)

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
    

    def update_after_login(self, new_ip):
        self.login_count = self.login_count +1
        self.last_login_ip = new_ip
        self.last_login_at = datetime.now()
        self.save()