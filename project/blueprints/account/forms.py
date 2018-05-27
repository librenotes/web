from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, TextAreaField
from wtforms.validators import InputRequired, Length


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Current Password", validators=[InputRequired('Please enter your password.')])
    new_password = PasswordField("New Password", validators=[InputRequired('Please enter your new password.'),
                                                             Length(min=3, max=25,
                                                                    message="Your password length must be consist of at least 3, at most 25 characters.")])
    re_new_password = PasswordField("Repeat New Password",
                                    validators=[InputRequired('Please enter your new password again.'),
                                                validators.EqualTo('re_new_password', message='Passwords must match')])


class ChangeDescription(FlaskForm):
    description = TextAreaField("Enter new description",
                                validators=[InputRequired('Please enter a description about your notes')])
