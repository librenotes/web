from project import app, cache, db, login_manager
from flask import render_template, redirect, url_for, request, session, flash, abort
from flask_login import login_user, current_user, login_required, logout_user
from .forms import RegisterForm, LoginForm, NoteForm
from .models import User, Note, Category
from werkzeug.security import generate_password_hash, check_password_hash
from re import split


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
    categories = []
    rand_key = session.get("rand_key")

    if user_.is_authenticated and user_.username == username and check_password_hash(user_.random_hashed, session.get("rand_key")):
        for note in Note.query.filter_by(user=user_).all():
            note.decrypt(rand_key)
            notes.append(note)
        for category in user_.categories:
            categories.append(category)
    else:
        searched_user = User.query.filter_by(username=username).first()
        if searched_user is not None:
            notes = Note.query.filter_by(user=searched_user, isprivate=False).all()
            categories = Category.query.filter_by(isprivate=False).filter(Category.users.any(User.id == searched_user.id)).all()
        else:
            abort(404)
    return render_template("notes.html.j2", notes=notes)


@app.route("/new_test", methods=['GET'])
@login_required
def new():
    user_ = current_user
    user_ = User.query.filter_by(id=user_.id).first()
    if check_password_hash(user_.random_hashed, session.get("rand_key")):
        for i in range(10):
            note = Note()
            note.title = "This is the {}. note's title".format(i)
            note.content = "And this is the content of {}".format(i)
            note.isprivate = True if i % 2 == 0 else False
            db.session.add(note)
            categories = split(r' ?#', "#And #we #have #crazy #categories #{}".format(i).lower())
            categories.remove('')
            if not note.isprivate:
                categories.append('public')
            for category_name in categories:
                if note.isprivate:
                    category = Category(name=category_name, isprivate=note.isprivate)
                else:
                    category = Category.query.filter_by(name=category_name).first()
                    if category is None:
                        category = Category(name=category_name, isprivate=note.isprivate)
                db.session.add(category)
                category.notes.append(note)
                category.users.append(user_)
            note.encrypt(session.get("rand_key"))
            user_.notes.append(note)
        db.session.commit()
        return 'OK'
    else:
        return "YOU ARE FAKE!!!"


@app.route("/logout")
@login_required
def logout():
    session.pop('rand_key')
    logout_user()
    return 'OK'


@app.route("/dbc")
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


def user_categories(username):
    user_ = current_user
    categories = []
    if user_.is_authenticated and user_.username == username and check_password_hash(user_.random_hashed, session.get("rand_key")):
        rand_key = session.get("rand_key")
        for category in user_.categories:
            category.decrypt(rand_key)
            categories.append(category)
    else:
        searched_user = User.query.filter_by(username=username)
        if searched_user:
            categories = Category.query.filter_by(isprivate=False).filter(Category.users.any(User.id == searched_user.id)).all()
    return categories


@app.route("/notes/<username>/<category_name>")
def filter_cat(username, category_name):
    user_ = current_user
    category_name = category_name.lower()
    notes = []
    if user_.is_authenticated and user_.username == username and check_password_hash(user_.random_hashed, session.get("rand_key")):
        rand_key = session.get("rand_key")
        for category in user_.categories.all():
            category.decrypt(rand_key)
            if category.name == category_name:
                notes_ = Note.query.filter_by(user=user_).filter(Note.categories.any(Category.id == category.id)).all()
                for note in notes_:
                    note.decrypt(rand_key)
                    notes.append(note)
        return render_template("notes.html.j2", notes=notes)
    else:
        searched_user = User.query.filter_by(username=username).first()
        if searched_user is not None:
            for note in Note.query.filter_by(isprivate=False, user=searched_user).filter(Note.categories.any(Category.name == category_name)).all():
                notes.append(note)

            return render_template("notes.html.j2", notes=notes)
        else:
            abort(404)
    return render_template("notes.html.j2")
