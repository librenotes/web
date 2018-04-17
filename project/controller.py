from project import app, db
from .models import User, Note, Category
from flask import render_template, flash

@app.route("/")
def index():
    flash("Message", "category")
    return render_template("register.html.j2")

@app.route("/login")
def login():
    return render_template("login.html.j2")

@app.route("/notesof/<user>")
def notes(user):
    return render_template("notes.html.j2")

@app.route("/dbc")
def createdb():
    db.create_all()
    return "OK"
