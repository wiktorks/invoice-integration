from flask import Flask
from .routes.main import main
from .routes.auth import auth
from .config import DevConfig
from .extensions import jwt, mail
from datetime import timedelta, datetime


def create_app(config_class=DevConfig):
    app = Flask(__name__, static_url_path="/public", static_folder="public")
    app.config.from_object(config_class)
    jwt.init_app(app)
    mail.init_app(app)

    @app.template_filter("strftime")
    def seconds_to_hours(timestamp):
        return str(timedelta(seconds=int(timestamp)))
    
    @app.template_filter("date_pretty")
    def timestamp_to_date(timestamp):
        date = int(float(timestamp)/1000)
        return str(datetime.fromtimestamp(date).date())

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
