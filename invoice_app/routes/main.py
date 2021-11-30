from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from flask_mailing import Message
from ..utils.clickup_reader import ClickupReader
from ..extensions import mail
from ..tasks.tasks import send_mail_report
import json, pdfkit


main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
@jwt_required()
def index():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    cr = ClickupReader()
    invoice_data = cr.get_billed_tasks(start_date=start_date, end_date=end_date)

    return render_template(
        "index.html",
        invoice_data=invoice_data,
        current_user=current_user,
    )


@main.route("/sendmail", methods=["POST"])
@jwt_required()
def send_mail():
    data = json.loads(request.data)
    mail_template = render_template("mail-view.html", data=data)
    if request.args.get('view'):
        return render_template("mail-view.html", data=data, view_only=True)
    
    else:
        send_mail_report.delay(mail_template)
        return jsonify({"message": "success"}), 200
