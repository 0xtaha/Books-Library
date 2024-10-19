from flask import Flask
from flask_restx import Api as ApiRestx
from flask_jwt_extended import JWTManager
from .default_config import DefaultConfig
from .api.support.security import authorizations
from .connections_handeller import DBConnector
from .models import User , Book, Review
from .routes import register_endpoints_routes

def create_app():
    app = Flask(__name__)

    DefaultConfig.init_loggers()
    
    app.config.from_object(DefaultConfig)

    apix = ApiRestx(
        app,
        prefix=DefaultConfig.PREFIX_PATH,
        title="backend",
        security="apikey",
        authorizations=authorizations,
    )

    
    JWTManager(app)

    register_endpoints_routes(apix)

    return app


def create_tables():
    db_connector = DBConnector()
    db = db_connector.pg_db
    db.create_tables(
        [
            User,
            Book,
            Review
        ]
    )