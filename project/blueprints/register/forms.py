from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired('Please enter your username.')])
    password = PasswordField("Password", validators=[InputRequired('Please enter your password.'),
                                                     validators.EqualTo('re_password', message='Passwords must match'),
                                                     validators.Length(min=3, max=25, message="Your password length must be consist of at least 3, at most 25 characters.")])
    re_password = PasswordField("Password Again", validators=[InputRequired('Please enter your password again.')])
    email = EmailField("Email", validators=[InputRequired('Please enter your email address.'),
                                            Email('This email address does not seem valid.')])
