import os, datetime


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_COOKIE_SECURE = True if os.environ.get("JWT_SECRET_KEY") == "True" else False
    SESSION_COOKIE_SECURE = (
        True if os.environ.get("JWT_SECRET_KEY") == "True" else False
    )
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
