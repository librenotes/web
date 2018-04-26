from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from .config import Config as conf
from flask_cache import Cache
from flask_login import LoginManager, login_required, logout_user
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object(conf)
Markdown(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
login_manager = LoginManager()
login_manager.init_app(app=app)
db = SQLAlchemy(app)


from project.blueprints.login.controller import bp_login as login_module
from project.blueprints.register.controller import bp_register as register_module
from project.blueprints.notes.controller import bp_notes as notes_module

app.register_blueprint(login_module)
app.register_blueprint(register_module)
app.register_blueprint(notes_module)

from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.errorhandler(403)
def unauthorized(e):
    # return render_template("page-404.html.j2")
    return str(403)


@app.errorhandler(404)
def unauthorized(e):
    # return render_template("page-404.html.j2")
    return str(404)

@app.route("/logout")
@login_required
def logout():
    session.pop('rand_key')
    logout_user()
    return 'OK'


@app.route("/")
def index():
    return render_template("index.html.j2")
