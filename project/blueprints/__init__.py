from project.models import Note, User, Category
from flask import session, flash, render_template
from werkzeug.security import check_password_hash
from re import split
from flask_mail import Message
from project import mail, MailConfirmer

class NoteHelper:
    @staticmethod
    def get_user_notes(user_):
        notes = []
        for note in Note.query.filter_by(user=user_).order_by(Note.updated_on.desc()).all():
            note_ = note.decrypt(AuthHelper.get_random_key())
            notes.append(note_)
        return notes

    @staticmethod
    def get_searched_user_notes(username):
        notes = []
        searched_user = User.query.filter_by(username=username).first()

        if searched_user is not None:
            for note in Note.query.filter_by(user=searched_user, isprivate=False) \
                    .order_by(Note.updated_on.desc()).all():
                note_ = note.decrypt(AuthHelper.get_random_key())
                notes.append(note_)
            return notes

        else:
            return None

    @staticmethod
    def get_user_note_with_id(user_, id_):
        note = Note.query.filter_by(user=user_, id=id_).first()
        return note


class CategoryHelper:
    @staticmethod
    def split_and_filter(category_list, filter_value):
        splitted_list = split(r' ?#', category_list)
        filter(lambda x: x is not filter_value, splitted_list)
        return splitted_list

    @staticmethod
    def get_new_categories(splitted_list, privacy):
        categories = []
        for category_name in splitted_list:
            category = Category(name=category_name, isprivate=privacy)
            categories.append(category)

        return categories


class AuthHelper:

    @staticmethod
    def check_session_validation(user_):
        return check_password_hash(user_.random_hashed, AuthHelper.get_random_key())

    @staticmethod
    def set_random_key(random_key):
        session['rand_key'] = random_key

    @staticmethod
    def get_random_key():
        return session.get("rand_key")

    @staticmethod
    def check_username(user_, username):
        return user_.username == username

    @staticmethod
    def check_password(user_, password):
        if check_password_hash(user_.password, password):
            return True
        else:
            return False

    @staticmethod
    def check_user_exist(email, username):
        exist = User.query.filter((User.username == username) | (User.email == email)).first()
        if exist:
            return True
        else:
            return False


class Flasher:
    @staticmethod
    def flash_errors(form, category):
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ), category=category)

    @staticmethod
    def flash(text_to_be_flashed, category):
        flash(text_to_be_flashed, category)


class Mailer:
    @staticmethod
    def send_confirmation_mail(username, reciepent):
        token = MailConfirmer.generate_confirmation_token(reciepent)
        msg = Message(recipients=[reciepent])
        msg.html = render_template("confirmation_mail.html.j2", username=username, token=token)
        mail.send(msg)
