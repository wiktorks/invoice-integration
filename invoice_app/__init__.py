from flask import Flask
from .routes.main import main
from .routes.auth import auth
from .config import DevConfig
from .extensions import jwt, mail


def create_app(config_class=DevConfig):
    app = Flask(__name__, static_url_path="/public", static_folder="public")
    app.config.from_object(config_class)
    jwt.init_app(app)
    mail.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
