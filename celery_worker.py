from invoice_app import celery
from invoice_app.app_factory import create_app
from invoice_app.utils.celery import init_celery

app = create_app()
init_celery(celery=celery, app=app)