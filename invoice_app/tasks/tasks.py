from flask.scaffold import F
from invoice_app import celery
import pdfkit
from flask_mailing import Message
from ..extensions import mail
import asyncio


@celery.task
def send_mail_report(mail_template):
    pdf_report = pdfkit.from_string(mail_template, False)

    message = Message(
        subject="Flask-Mailing module",
        recipients=["invoiceflask@gmail.com"],
        body="Wygenerowany raport PDF w załączniku.",
    )
    message.attach("raport.pdf", pdf_report)
    asyncio.run(mail.send_message(message), debug=True)