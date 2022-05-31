import logging

from flask import Flask
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

compress = Compress()
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address, default_limits=["1 per second"])
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    compress.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    from app.thing import bp as thing_bp
    from app.user import bp as user_bp

    app.register_blueprint(auth_bp, url_prefix="/v1/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(thing_bp, url_prefix="/v1/things")
    app.register_blueprint(user_bp, url_prefix="/v1/users")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Startup")

    return app


from app import models, user  # noqa: E402, F401
