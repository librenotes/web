from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Email


class ContactForm(FlaskForm):
    name = StringField("Your Name", validators=[InputRequired("Please enter a name.")])
    email = StringField("Your Email", validators=[InputRequired("Please enter a mail address."),
                                                  Email("This is not a valid mail address.")])
    message = TextAreaField("Your Message", validators=[InputRequired("Please enter a message")])
