from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Current Password", validators=[InputRequired('Please enter your password.')])
    new_password = PasswordField("New Password", validators=[InputRequired('Please enter your new password.')])
    re_new_password = PasswordField("Repeat New Password",
                                    validators=[InputRequired('Please enter your new password again.'),
                                                validators.EqualTo('re_new_password', message='Passwords must match')])
