from .models import Note, User, Category
from flask import session, flash, render_template
from werkzeug.security import check_password_hash
from re import split
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
import requests


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
            return notes, searched_user

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
        return check_password_hash(user_.password, password)

    @staticmethod
    def check_user_exist(email, username):
        exist = User.query.filter((User.username == username) | (User.email == email)).first()
        return True if exist else False


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
    def __init__(self):
        self.app = None
        self.mail = None

    def init_app(self, app, mail):
        self.app = app
        self.mail = mail

    def send_confirmation_mail(self, username, recipient):
        token = self.generate_confirmation_token(recipient)
        msg = Message(recipients=[recipient])
        msg.html = render_template("confirmation_mail.html.j2", username=username, token=token)
        msg.subject = "Validate Your Account"
        self.mail.send(msg)

    def generate_confirmation_token(self, email):
        serializer = URLSafeTimedSerializer(self.app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=self.app.config['SECURITY_PASSWORD_SALT'])

    def confirm_token(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(self.app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=self.app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        return email


def fetch_github_pictures(url, path):
    with requests.get(url) as resp:
        with open(path, "wb") as f:
            f.write(resp.content)


class CommitFeedFetcher:
    _FEED_KEY = "commit_feed"
    _i = 0

    def __init__(self, cache=None):
        self.cache = cache

    def init_cache(self, cache):
        self.cache = cache

    def update(self, count=15):
        feed = []
        content_json = requests.get("https://api.github.com/repos/librenotes/web/commits").json()
        for i in range(0, count):
            message = content_json[i]["commit"]["message"]
            author = content_json[i]["commit"]["committer"]["name"]
            url = content_json[i]["html_url"]
            feed.append((author, message, url))
        self.cache.set(self._FEED_KEY, feed)

    def get(self):
        return self.cache.get(self._FEED_KEY)
