from project import app, db
from .models import User, Note, Category
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html.j2")

@app.route("/login")
def login():
    return render_template("login.html.j2")

@app.route("/notesof/<user>")
def notes(user):
    return render_template("notes.html.j2")

@app.route("/dbc")
def createdb():
    return "OK"
