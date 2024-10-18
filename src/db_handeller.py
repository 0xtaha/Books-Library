import peewee, os
from flask import current_app


class DBConnector:

    _instance = None

    def __new__(cls,) -> None:
        if cls._instance is None:
            cls._instance = super(DBConnector, cls).__new__(cls)
            cls.pg_db = peewee.PostgresqlDatabase(
                database=os.environ["POSTGRESQL_DB_NAME"],
                user=os.environ["POSTGRESQL_DB_USER"],
                password=os.environ["POSTGRESQL_DB_PASSWD"],
                host=os.environ["POSTGRESQL_DB_HOST"],
                port=os.environ["POSTGRESQL_DB_PORT"],
                sslmode='disable',
                autorollback=True,
            )

        return cls._instance


