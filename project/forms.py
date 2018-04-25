from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, HiddenField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import EmailField

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired('Please enter your username.')])
    password = PasswordField("Password", validators=[InputRequired('Please enter your password.'),  validators.EqualTo('re_password', message='Passwords must match')])
    re_password = PasswordField("Password Again", validators=[InputRequired('Please enter your password again.')])
    email = EmailField("Email", validators=[InputRequired('Please enter your email address.'),
                                            Email('This email address does not seem valid.')])


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired('Please enter your username.')])
    password = PasswordField("Password", validators=[InputRequired('Please enter your password.')])


class NoteForm(FlaskForm):
    id = HiddenField('ID')
    title = StringField("Title", validators=[InputRequired("You can't leave title area empty")])
    content = StringField("Content", validators=[InputRequired("You can't leave content area empty.")], widget=TextArea())
    categories = StringField("Categories")
    isprivate = BooleanField("Is Private")


class DeleteNoteForm(FlaskForm):
    id = HiddenField('ID')
