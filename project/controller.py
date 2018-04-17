<<<<<<< HEAD
from project import app, db
from .models import User, Note, Category
from flask import render_template
=======
from project import app, cache
from flask import render_template, redirect, url_for, request
from .forms import RegisterForm, LoginForm

>>>>>>> 2599b24... created post methods for login and form

@app.route("/")
def index():
    return render_template("index.html.j2")


@app.route("/register", methods=["GET"])
def register_get():
    return render_template("register.html.j2")


@cache.cached()
@app.route("/login", methods=["POST"])
def login_get():
    return render_template("login.html.j2")


@app.route("/signin", methods=["POST"])
def login_post():
    form = LoginForm(request.form)
    if form.validate():
        
    # TODO: check credentials
    # TODO: decrypt note_encryption_key using password
    # TODO: put decrypted note_encryption_key to session
    return redirect(url_for('index'))


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
