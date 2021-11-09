from flask import Flask, render_template
from .utils.excel_reader import ExcelReader
import os


def create_app():
    app = Flask(__name__, static_url_path="/public", static_folder='public')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    @app.route("/", methods=["GET"])
    def index():
        excel_path = os.path.join(app.root_path, "daily_report_28_10_2021_v2.xlsx")
        er = ExcelReader(excel_path)
        invoice_data = er.get_total_hours_by_project()
        return render_template("index.html", invoice_data=invoice_data)

    return app
