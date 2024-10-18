import peewee, os, redis
from .default_config import DefaultConfig

class DBConnector:

    _instance = None

    def __new__(cls,) -> None:
        if cls._instance is None:
            cls._instance = super(DBConnector, cls).__new__(cls)
            cls.pg_db = peewee.PostgresqlDatabase(
                database=DefaultConfig.DATABASE["name"],
                user=DefaultConfig.DATABASE["user"],
                password=DefaultConfig.DATABASE["password"],
                host=DefaultConfig.DATABASE["host"],
                port=DefaultConfig.DATABASE["port"],
                sslmode='disable',
                autorollback=True,
            )

        return cls._instance


class RedisConnector:
    _instance = None

    def __new__(cls,) -> None:
        if cls._instance is None:
            cls._instance = super(RedisConnector, cls).__new__(cls)
            cls.rdb : redis.Redis = redis.Redis(
                host= DefaultConfig.REDIS['host'],
                port= DefaultConfig.REDIS['port'],
                db= DefaultConfig.REDIS['db'],
                password= DefaultConfig.REDIS['password']
            )

        return cls._instance
