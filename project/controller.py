from project import app, cache, login_manager
from flask import render_template, redirect, url_for, request, session, flash
from flask_login import login_user, current_user, login_required, logout_user
from .forms import RegisterForm, LoginForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from Crypto.Cipher import AES


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), category='danger')


@app.route("/")
def index():
    return render_template("index.html.j2")


@app.route("/register", methods=["GET"])
def register_get():
    return render_template("register.html.j2")


@cache.cached()
@app.route("/login", methods=["POST"])
def login_get():
    form = LoginForm()
    return render_template("login.html.j2", form=form)


@app.route("/signin", methods=["POST"])
def login_post():
    form = LoginForm(request.form)
    if form.validate():
        user_ = User.query.filter_by(username=form.username).first()
        if user_ and check_password_hash(user_.password, form.password):
            login_user(user_)
            cipher = AES.new(form.password, AES.MODE_CBC)
            rand_key = cipher.decrypt(user_.random_encrypted)
            session['rand_key'] = rand_key
            flash('Login Successful!', category='success')
            return redirect(url_for(notes, user=form.username))
        else:
            flash('Password or Username does not match', category='danger')
            return redirect(url_for(login_get))
    else:
        flash_errors(form)
        return redirect(url_for(login_get))


@app.route("/signup", methods=["POST"])
def register_post():
    # TODO: create a random key(note_encryption_key) to encrypt and decrypt notes
    # TODO: hash note_encryption_key using password, save it to user table as note_encryption_key
    # TODO: create md5 of note_encryption_key
    # TODO: save user
    pass


@app.route("/notes/<user>")
def notes(user):
    return render_template("notes.html.j2")


@app.route("/dbc")
def createdb():
    return "OK"
