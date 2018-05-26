import requests
from flask import render_template, redirect, url_for, request, Blueprint, session, json
from project.models import User, ContactMessage
from .forms import ContactForm
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from project.helpers import Flasher
from project import db, cache

bp_index = Blueprint('app_index', __name__)


@bp_index.route("/logout")
@login_required
def logout():
    session.pop('rand_key')
    logout_user()
    Flasher.flash("You are successfully logged out!", "success")
    return redirect(url_for(".index"))


@bp_index.route("/", methods=["GET"])
def index():
    form = ContactForm()
    github_feed = get_commit_messages()
    return render_template("index.html.j2", form=form, github_feed=github_feed)


@bp_index.route("/contact", methods=["POST"])
def contact():
    form = ContactForm(request.form)
    if form.validate():
        c = ContactMessage()
        c.sender_name = form.name.data
        c.sender_mail = form.email.data
        c.message = form.message.data
        db.session.add(c)
        db.session.commit()
        Flasher.flash("Your message is sent to the developers", 'success')
    else:
        Flasher.flash_errors(form, "danger")
    return redirect(url_for('app_index.index'))


@bp_index.route("/dbc")
def createdb():
    db.drop_all()
    db.create_all()
    user = User()
    user.username = 'asd'
    user.password = generate_password_hash('asd')
    user.email = 'asd@gmail.com'
    user.generate_encryption_keys('asd')
    db.session.add(user)
    db.session.commit()
    login_user(user)
    session['rand_key'] = user.get_random_key('asd')
    return "OK"


@cache.memoize(timeout=900)
def get_commit_messages(count=15):
    feed = []
    content = requests.get("https://api.github.com/repos/librenotes/web/commits").content
    content_json = json.loads(content)
    for i in range(0, count):
        message = content_json[i]["commit"]["message"]
        author = content_json[i]["commit"]["committer"]["name"]
        url = content_json[i]["commit"]["url"]
        feed.append((author, message, url))
    return feed
