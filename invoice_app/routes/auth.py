from flask import Blueprint, url_for, redirect, render_template, flash
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    current_user,
    verify_jwt_in_request,
    get_jwt_identity,
)
import re

from ..forms.login_form import LoginForm

auth = Blueprint("auth", __name__)


@auth.after_request
def refresh_expiring_jwts(response):
    try:
        if not re.search("login=True", response.location):
            raise Exception
        
        verify_jwt_in_request()
        access_token = create_access_token(identity=get_jwt_identity())
        set_access_cookies(response, access_token)
        return response
    except Exception:
        return response


@auth.route("/login", methods=["GET", "POST"])
@jwt_required(optional=True)
def login():
    if current_user:
        return redirect(url_for("main.index"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if (
            login_form.username.data == "Wiktor"
            and login_form.password.data == "secretpassword"
        ):
            response = redirect(url_for("main.index"))
            access_token = create_access_token(identity=login_form.username.data)
            set_access_cookies(response, access_token)
            flash("You have successfully logged in!", "success")
            return response
        else:
            flash("Login unsuccessfull. Please provide valid credentials.", "danger")

    return render_template("login.html", title="Login", form=login_form)


@auth.route("/logout")
def logout():
    response = redirect(url_for("auth.login", logout=True))
    unset_jwt_cookies(response)
    return response
