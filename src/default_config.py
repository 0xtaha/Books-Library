#!/usr/bin/env python
# encoding: utf-8

import os
from logging.config import dictConfig
from dotenv import load_dotenv


class DefaultConfig:
    load_dotenv(".env")

    DEBUG = os.environ.get("DEBUG")
    BUNDLE_ERRORS = True

    SECURITY_PASSWORD_HASH = "sha512_crypt"

    PREFIX_PATH = "/{}".format(os.environ.get("DEPLOYMENT_VERSION"))



    DATABASE = {
        "name": os.environ.get("POSTGRESQL_DB_NAME"),
        "engine": os.environ.get("POSTGRESQL_DB_ENGINE"),
        "user": os.environ.get("POSTGRESQL_DB_USER"),
        "password": os.environ.get("POSTGRESQL_DB_PASSWD"),
        "host": os.environ.get("POSTGRESQL_DB_HOST"),
        "port": os.environ.get("POSTGRESQL_DB_PORT"),
    }

    REDIS = {
        'host' : os.environ.get("REDIS_CONFIG_HOST"),
        'port' : os.environ.get('REDIS_CONFIG_PORT'),
        'db' : os.environ.get('REDIS_CONFIG_DB'),
        'password' : os.environ.get('REDIS_CONFIG_PASSWORD')
    }

    JWT_EXPIRE = {
        'hours' : int(os.environ.get("JWT_EXPIRE_HOURS")),
        'mins' : int(os.environ.get("JWT_EXPIRE_MINUTES")),
        'sec' : int(os.environ.get("JWT_EXPIRE_SECONDS")),
    }

    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY")

    # PROPAGATE_EXCEPTIONS = True

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

    

    @staticmethod
    def init_loggers():
        LOGGING = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": (
                        "%(levelname)s -- %(asctime)s --"
                        " %(pathname)s:%(lineno)d >  %(message)s "
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "verbose",
                }
            },
            "loggers": {
                "backend": {
                    "level": "DEBUG",
                    "handlers": ["console"],
                }
            },
        }
        dictConfig(LOGGING)
