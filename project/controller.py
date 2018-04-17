from project import app, cache, db
from flask import render_template, redirect, url_for, request, session, flash
from flask_login import login_user, current_user, login_required, logout_user
from .forms import RegisterForm, LoginForm
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from Crypto.Cipher import AES
from Crypto import Random


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), category='danger')


def get_padded_passwords(password):
    remainder = 16 - len(password) % 16
    padded_plain = password + '0' * remainder
    hashed_password = generate_password_hash(password)
    padded_hashed = hashed_password[-16:]
    return padded_plain, padded_hashed


@app.route("/")
def index():
    return render_template("index.html.j2")


@app.route("/register", methods=["GET"])
def register_get():
    form = RegisterForm()
    return render_template("register.html.j2", form=form)


@cache.cached()
@app.route("/login", methods=["GET"])
def login_get():
    form = LoginForm()
    return render_template("login.html.j2", form=form)


@app.route("/signin", methods=["POST"])
def login_post():
    form = LoginForm(request.form)
    if form.validate():
        user_ = User.query.filter_by(username=form.username.data).first()
        if user_ and check_password_hash(user_.password, form.password.data):
            login_user(user_)
            padded_plain, padded_hashed = get_padded_passwords(form.password.data)
            cipher = AES.new(padded_plain, AES.MODE_CBC, padded_hashed)
            rand_key = cipher.decrypt(user_.random_encrypted)
            session['rand_key'] = rand_key
            flash('Login Successful!', category='success')
            return redirect(url_for('notes', user=form.username.data))
        else:
            flash('Password or Username does not match', category='danger')
            return redirect(url_for("login_get"))
    else:
        flash_errors(form)
        return redirect(url_for("login_get"))


@app.route("/signup", methods=["POST"])
def register_post():
    form = RegisterForm(request.form)
    if form.validate():
        user_ = User.query.filter_by(username=form.username.data).first()
        email_ = User.query.filter_by(email=form.email.data).first()
        if not (user_ or email_):   # check if username or email address already exists.
            rand_key = Random.get_random_bytes(256)
            padded_plain, padded_hashed = get_padded_passwords(form.password.data)
            print(len(padded_hashed))
            print(len(padded_plain))
            cipher = AES.new(padded_plain, AES.MODE_CBC, padded_hashed)
            random_encrypted = cipher.encrypt(rand_key)
            user = User()
            user.username = form.username.data
            user.password = generate_password_hash(form.password.data)
            user.email = form.email.data
            user.random_hashed = generate_password_hash(rand_key)
            user.random_encrypted = random_encrypted
            db.session.add(user)
            db.session.commit()
            flash('Register Successful!', category='success')
            return redirect(url_for('login_get'))
        else:
            flash('This username or email address is already in use', category='warning')
    else:
        flash_errors(form)
    return redirect(url_for('register_get'))


@login_required
@app.route("/notes/<user>")
def notes(user):
    return render_template("notes.html.j2")


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return 'OK'


@app.route("/dbc")
def createdb():
    db.create_all()
    return "OK"
