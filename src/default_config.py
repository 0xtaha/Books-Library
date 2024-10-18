#!/usr/bin/env python
# encoding: utf-8

import os
from logging.config import dictConfig
from dotenv import load_dotenv
from .db_handeller import DBConnector
from .models import User


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

    # PROPAGATE_EXCEPTIONS = True

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

    @staticmethod
    def create_tables():
        db_connector = DBConnector()
        db = db_connector.pg_db
        db.create_tables(
            [
                User
            ]
        )

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
