from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[Required(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[Required(), Length(min=5, max=30)])
    # remember_me = BooleanField("Remember me")
    submit = SubmitField("Log in")
