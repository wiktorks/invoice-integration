from flask_jwt_extended import JWTManager
from flask_mailing import Mail
from flask import redirect, url_for, flash

jwt = JWTManager()
mail = Mail()


@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    flash("You must log in to use this app.", "info")
    return redirect(url_for("auth.logout"))


@jwt.expired_token_loader
def custom_expired_response(header, payload):
    return redirect(url_for("auth.logout"))


@jwt.invalid_token_loader
def invalid_token_callback(_err):
    return redirect(url_for("auth.logout"))


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return {"name": identity}
