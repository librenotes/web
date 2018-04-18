from project import app, cache, db, login_manager
from flask import render_template, redirect, url_for, request, session, flash, abort
from flask_login import login_user, current_user, login_required, logout_user
from .forms import RegisterForm, LoginForm, NoteForm
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash

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
    if current_user.is_authenticated:
        flash("You are already logged in", "success")
        return redirect(url_for('notes', username=current_user.username))
    else:
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
            return redirect(url_for('notes', username=form.username.data))
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
            user.username = form.username.data
            user.password = generate_password_hash(form.password.data)
            user.email = form.email.data
            user.generate_encryption_keys(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            session['rand_key'] = user.get_random_key(form.password.data)
            flash('Register Successful, now you are logged in!', category='success')
            return redirect(url_for('notes', username=form.username.data))
        else:
            flash('This username or email address is already in use', category='warning')
    else:
        flash_errors(form)
    return redirect(url_for('register_get'))


@app.route("/notes/<username>")
def notes(username):
    user_ = current_user
    notes = []
    if user_.is_authenticated and user_.username == username and check_password_hash(user_.random_hashed, session.get("rand_key")):
        for note in Note.query.filter_by(user=user_).all():
            note.decrypt(session.get("rand_key"))
            notes.append(note)
        return render_template("notes.html.j2", notes=notes)
    else:
        searched_user = User.query.filter_by(username=username).first()
        if searched_user is not None:
            notes =  Note.query.filter_by(user=searched_user, isprivate=False).all()
            return render_template("notes.html.j2", notes=notes)
        else:
            abort(404)
    return render_template("notes.html.j2")


@app.route("/new_test", methods=['GET'])
@login_required
def new():
    user_ = current_user
    user_ = User.query.filter_by(id=user_.id).first()
    print(user_.notes)
    if check_password_hash(user_.random_hashed, session.get("rand_key")):
        for i in range(10):
            note = Note()
            note.title = "This is the {}. note's title".format(i)
            note.content = "And this is the content of {}".format(i)
            note.categories = "#And #we #have #crazy #categories #{}".format(i)
            note.isprivate = True if i % 2 == 0 else False
            note.encrypt(session.get("rand_key"))
            db.session.add(note)
            user_.notes.append(note)
        db.session.commit()
        return 'OK'
    else:
        return "FUCK MY ASS"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return 'OK'


@app.route("/dbc")
def createdb():
    db.drop_all()
    db.create_all()
    return "OK"
