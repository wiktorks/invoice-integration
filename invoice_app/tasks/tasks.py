from invoice_app import celery
from invoice_app.extensions import mail
from flask_mailing import Message
import asyncio, pdfkit


@celery.task
def send_mail_report(mail_template, project_name):
    message = Message(
        subject="Flask-Mailing module",
        recipients=["invoiceflask@gmail.com"],
        body="Wygenerowany raport PDF w załączniku.",
    )
    if isinstance(mail_template, list):
        for idx, template in enumerate(mail_template):
            pdf_report = pdfkit.from_string(template, False)
            message.attach(f"{project_name[idx]}.pdf", pdf_report)
    else:
        pdf_report = pdfkit.from_string(mail_template, False)
        message.attach(f"{project_name}.pdf", pdf_report)

    asyncio.run(mail.send_message(message), debug=True)
