from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    # This is where the routes would be registered, blueprints are ideal.

    from .api_1_0 import api_blueprint as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint)

    return app
