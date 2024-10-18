from flask import Flask
from flask_restx import Api as ApiRestx
from .api.routes import register_endpoints_routes
from .default_config import DefaultConfig
from .security import api_key_authorizations

def create_app():
    app = Flask(__name__)

    DefaultConfig.init_loggers()
    DefaultConfig.create_tables()
    
    app.config.from_object(DefaultConfig)

    apix = ApiRestx(
        app,
        prefix=DefaultConfig.PREFIX_PATH,
        title="backend",
        security="apikey",
        authorizations=api_key_authorizations,
    )

    register_endpoints_routes(apix)

    return app
