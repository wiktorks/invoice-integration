from flask import Flask
from datetime import timedelta, datetime
from .routes.main import main
from .routes.auth import auth
from .config import DevConfig
from .extensions import jwt, mail
from .utils.celery import init_celery


def create_app(config_class=DevConfig, **kwargs):
    app = Flask(__name__, static_url_path="/public", static_folder="public")
    app.config.from_object(config_class)
    jwt.init_app(app)
    mail.init_app(app)
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)

    @app.template_filter("strftime")
    def seconds_to_hours(timestamp):
        return str(timedelta(seconds=int(timestamp)))
    
    @app.template_filter('seconds_to_days')
    def seconds_to_days(timestamp):
        dt = timedelta(seconds=int(timestamp))
        secs_per_day = 24*60*60    # hours * mins * secs
        return dt.total_seconds()/secs_per_day

    @app.template_filter("date_pretty")
    def timestamp_to_date(timestamp):
        date = int(float(timestamp) / 1000)
        return str(datetime.fromtimestamp(date).date())

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
