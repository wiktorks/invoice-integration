import os, datetime

class DevConfig:
    def __init__(self) -> None:
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        self.JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
        self.JWT_COOKIE_SECURE = False
        self.SESSION_COOKIE_SECURE = False
        self.JWT_TOKEN_LOCATION = ["cookies"]
        self.JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
        
        self.MAIL_SERVER="smtp.googlemail.com"
        self.MAIL_PORT = 587
        self.MAIL_USE_TLS = True
        self.MAIL_USE_SSL = False
        self.MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
        self.MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
        self.MAIL_FROM = os.environ.get("MAIL_USERNAME")


class ProdConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    
    MAIL_SERVER="smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_FROM = os.environ.get("MAIL_USERNAME")
