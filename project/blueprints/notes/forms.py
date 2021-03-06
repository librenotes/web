from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, validators, HiddenField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired


class NoteForm(FlaskForm):
    id = HiddenField('ID')
    title = StringField("Title", validators=[InputRequired("You can't leave title area empty")])
    content = StringField("Content", validators=[InputRequired("You can't leave content area empty.")],
                          widget=TextArea())
    categories = StringField("Categories")
    isprivate = BooleanField("Is Private")


class DeleteNoteForm(FlaskForm):
    id = HiddenField('ID')
