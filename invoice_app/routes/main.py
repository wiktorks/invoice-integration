from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_jwt_extended import jwt_required, current_user
from ..utils.excel_reader import ExcelReader

import os


main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
@jwt_required(optional=True)
def index():
    if current_user:
        excel_path = os.path.join(
            current_app.root_path, "daily_report_28_10_2021_v2.xlsx"
        )
        er = ExcelReader(excel_path)
        invoice_data = er.get_total_hours_by_project()
        return render_template(
            "index.html",
            invoice_data=invoice_data,
            current_user=current_user,
            session="True" if current_app.config["SESSION_COOKIE_SECURE"] else "False",
            jwt="True" if current_app.config["JWT_COOKIE_SECURE"] else "False",
        )
    else:
        flash("You must log in to use this app.", "info")
        return redirect(url_for("auth.login"))
