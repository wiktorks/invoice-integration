from flask import Flask, render_template, flash, redirect, url_for
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    unset_jwt_cookies,
    current_user,
)
from flask_jwt_extended.utils import set_access_cookies

from .utils.excel_reader import ExcelReader
from .forms.login_form import LoginForm
import os


def create_app():
    app = Flask(__name__, static_url_path="/public", static_folder="public")
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def custom_unauthorized_response(_err):
        return redirect(url_for("logout"))

    @jwt.expired_token_loader
    def custom_expired_response(header, payload):
        return redirect(url_for("logout"))

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return {"name": identity}

    # @app.after_request
    # def refresh_expiring_jwts(response):
    #     try:
    #         print()
    #         verify_jwt_in_request()
    #         access_token = create_access_token(identity=get_jwt_identity())
    #         set_access_cookies(response, access_token)
    #         return response
    #     except (RuntimeError, KeyError, ExpiredSignatureError, NoAuthorizationError):
    #         return response

    @app.route("/", methods=["GET"])
    @jwt_required(optional=True)
    def index():
        if current_user:
            excel_path = os.path.join(app.root_path, "daily_report_28_10_2021_v2.xlsx")
            er = ExcelReader(excel_path)
            invoice_data = er.get_total_hours_by_project()
            return render_template(
                "index.html", invoice_data=invoice_data, current_user=current_user
            )
        else:
            flash("You must log in to use this app.", "info")
            return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    @jwt_required(optional=True)
    def login():
        if current_user:
            return redirect(url_for("index"))
        login_form = LoginForm()
        if login_form.validate_on_submit():
            if (
                login_form.username.data == "Wiktor"
                and login_form.password.data == "secretpassword"
            ):
                response = redirect(url_for("index"))
                access_token = create_access_token(identity=login_form.username.data)
                set_access_cookies(response, access_token)
                flash("You have successfully logged in!", "success")
                return response
            else:
                flash(
                    "Login unsuccessfull. Please provide valid credentials.", "danger"
                )

        return render_template("login.html", title="Login", form=login_form)

    @app.route("/logout")
    def logout():
        response = redirect(url_for("login"))
        unset_jwt_cookies(response)
        return response

    return app
