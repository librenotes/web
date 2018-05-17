from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .config import Config as conf
from flask_login import LoginManager, login_required, logout_user, login_user
from werkzeug.security import generate_password_hash
from flask_debugtoolbar import DebugToolbarExtension
import bleach
import markdown2
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(conf)
login_manager = LoginManager()
login_manager.init_app(app=app)
db = SQLAlchemy(app)
mail = Mail(app)
# toolbar = DebugToolbarExtension(app)


class MailConfirmer:

    @staticmethod
    def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        return email


from project.blueprints.login.controller import bp_login as login_module
from project.blueprints.register.controller import bp_register as register_module
from project.blueprints.notes.controller import bp_notes as notes_module
from project.blueprints import Flasher
app.register_blueprint(login_module)
app.register_blueprint(register_module)
app.register_blueprint(notes_module)

from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.template_filter('markdown')
def clean(s):
    return markdown2.markdown(s)


@app.template_filter('linkify')
def linkify(s):
    return bleach.linkify(s)


@app.errorhandler(403)
def unauthorized(e):
    return redirect(url_for("index"))


@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for("index"))


@app.errorhandler(404)
def unauthorized(e):
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    session.pop('rand_key')
    logout_user()
    Flasher.flash("You are successfully logged out!", "success")
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html.j2")


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
