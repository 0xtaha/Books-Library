import peewee
from playhouse import shortcuts 
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


class Book(BaseModel):
    id = peewee.AutoField()
    title = peewee.CharField(max_length=255)
    # content should be BigBitField, but for simplecty let's assume it's a text
    content = peewee.TextField()

    def serialize_with_content(self):
        content = {
            field: getattr(self, field)
            for field in (
                "id",
                "title",
                "content",
            )
        }
        return content
    
    def serialize(self):
        content = {
            field: getattr(self, field)
            for field in (
                "id",
                "title",
            )
        }
        return content

class Review(BaseModel):
    id = peewee.AutoField()
    book = peewee.ForeignKeyField(Book, null=False, on_delete='CASCADE')
    user = peewee.ForeignKeyField(User, null=False, on_delete='CASCADE')
    desc = peewee.TextField(null=False)

    
    def serialize(self):
        to_exclude = (
            User.id,
            User.last_login_at,
            User.last_login_ip,
            User.active,
            User.password,
            User.login_count,
        )
        return shortcuts.model_to_dict(self, exclude=to_exclude)
