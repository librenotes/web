from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired('Please enter your username.')])
    password = PasswordField("Password", validators=[InputRequired('Please enter your password.'),
                                                     validators.Length(min=3, max=25, message="Your password length must be consist of at least 3, at most 25 characters.")])
