from flask import Flask, render_template, flash, redirect
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    unset_jwt_cookies
)
from flask_jwt_extended.utils import set_access_cookies

from .utils.excel_reader import ExcelReader
from .forms.login_form import LoginForm
import os


def create_app():
    app = Flask(__name__, static_url_path="/public", static_folder="public")
    jwt = JWTManager(app)

    @app.route("/", methods=["GET"])
    @jwt_required(optional=True)
    def index():
        current_identity = get_jwt_identity()
        if current_identity:
            excel_path = os.path.join(app.root_path, "daily_report_28_10_2021_v2.xlsx")
            er = ExcelReader(excel_path)
            invoice_data = er.get_total_hours_by_project()
            return render_template("index.html", invoice_data=invoice_data)
        else:
            flash("You must log in to use this app.", "info")
            return redirect("/login")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        login_form = LoginForm()
        if login_form.validate_on_submit():
            if (
                login_form.username.data == "Wiktor"
                and login_form.password.data == "secretpassword"
            ):
                response = redirect("/")
                access_token = create_access_token(identity=login_form.username.data)
                set_access_cookies(response, access_token)
                flash("You have successfully logged in!", "success")
                return response
            else:
                flash(
                    "Login unsuccessfull. Please provide valid credentials.", "danger"
                )

        return render_template("login.html", title="Login", form=login_form)
    
    @app.route('/logout')
    def logout():
        response = redirect('login')
        unset_jwt_cookies(response)
        return response

    return app
