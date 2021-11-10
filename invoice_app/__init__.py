from flask import Flask, redirect, url_for
from flask_jwt_extended import (
    JWTManager,
)
from invoice_app.routes.main import main
from invoice_app.routes.auth import auth
from invoice_app.config import Config
import os, datetime

jwt = JWTManager()


@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    return redirect(url_for("auth.logout"))


@jwt.expired_token_loader
def custom_expired_response(header, payload):
    return redirect(url_for("auth.logout"))


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return {"name": identity}


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path="/public", static_folder="public")
    app.config.from_object(config_class)

    jwt.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
