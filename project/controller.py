from project import app, cache, db, login_manager
from flask import render_template, redirect, url_for, request, session, flash
from flask_login import login_user, current_user, login_required, logout_user
from .forms import RegisterForm, LoginForm
from .models import User, AESCipher
from werkzeug.security import generate_password_hash, check_password_hash
from Crypto.Cipher import AES
from Crypto import Random

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


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
    form = RegisterForm()
    return render_template("register.html.j2", form=form)


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
            session['rand_key'] = user_.get_random_key(form.password.data)
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
            user = User()
            user.create_rand_key(form.password.data)
            user.username = form.username.data
            user.password = generate_password_hash(form.password.data)
            user.email = form.email.data
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Register Successful, now you are logged in!', category='success')
            return redirect(url_for('notes', user=form.username.data))
        else:
            flash('This username or email address is already in use', category='warning')
    else:
        flash_errors(form)
    return redirect(url_for('register_get'))


@app.route("/notes/<user>")
@login_required
def notes(user):
    return render_template("notes.html.j2")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return 'OK'


@app.route("/dbc")
def createdb():
    db.create_all()
    return "OK"
