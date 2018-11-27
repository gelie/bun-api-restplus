from flask import Flask
# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from .config import Config

db = SQLAlchemy()
ma = Marshmallow()
# migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    # migrate.init_app(app, db)

    from api import api
    app.register_blueprint(api, url_prefix='/bungeni/api/v1')

    # if not app.debug and not app.testing:
    # # ... no changes to logging setup
    # pass

    return app
