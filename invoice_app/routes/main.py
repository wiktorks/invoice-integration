from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from flask_mailing import Message
from ..utils.clickup_reader import ClickupReader
from ..extensions import mail
import json, pdfkit


main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
@jwt_required(optional=True)
def index():
    if current_user:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        cr = ClickupReader()
        invoice_data = cr.get_billed_tasks(start_date=start_date, end_date=end_date)

        return render_template(
            "index.html",
            invoice_data=invoice_data,
            current_user=current_user,
        )
    else:
        flash("You must log in to use this app.", "info")
        return redirect(url_for("auth.login"))


@main.route("/sendmail", methods=["POST"])
async def send_mail():
    data = json.loads(request.data)
    mail_template = render_template("mail-view.html", data=data)

    if request.args.get('view'):
        return render_template("mail-view.html", data=data, view_only=True)
    else:
        pdf_report = pdfkit.from_string(mail_template, False)

        message = Message(
            subject="Flask-Mailing module",
            recipients=["invoiceflask@gmail.com"],
            body="Wygenerowany raport PDF w załączniku.",
        )
        message.attach("raport.pdf", pdf_report)
        await mail.send_message(message)
        return jsonify({"message": "success"}), 200
