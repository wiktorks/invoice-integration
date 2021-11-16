from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_jwt_extended import jwt_required, current_user
from flask_mailing import Message
from ..utils.clickup_reader import ClickupReader
from ..extensions import mail
import os


main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
@jwt_required(optional=True)
def index():
    if current_user:
        cr = ClickupReader()
        invoice_data = cr.get_billed_tasks()
        return render_template(
            "index.html",
            invoice_data=invoice_data,
            current_user=current_user,
        )
    else:
        flash("You must log in to use this app.", "info")
        return redirect(url_for("auth.login"))
    
@main.route("/sendmail")
async def send_mail():
    message = Message(
        subject="Flask-Mailing module",
        recipients=["wiktorks1994@gmail.com"],
        body="This is the basic email body",
        )
    await mail.send_message(message)
    return redirect('main.index')
