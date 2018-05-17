from flask import Flask, render_template, session, redirect, url_for
from flask_login import LoginManager, login_required, logout_user, login_user
from werkzeug.security import generate_password_hash
from flask_mail import Mail
from .helpers import Mailer, Flasher
from .models import User, db
import bleach
import markdown2

login_manager = LoginManager()
mail = Mail()
mailer = Mailer()


def create_app(config):
    # Init app
    app = Flask(__name__)
    app.config.from_object(config)
    # Init extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    mailer.init_app(app, mail)
    # Registers
    register_blueprints(app)
    register_error_handlers(app)
    register_base_routes(app)
    register_template_filters(app)
    register_login_manager_handlers(app)
    return app


def register_blueprints(app):
    from project.blueprints.login.controller import bp_login as login_module
    from project.blueprints.register.controller import bp_register as register_module
    from project.blueprints.notes.controller import bp_notes as notes_module
    app.register_blueprint(login_module)
    app.register_blueprint(register_module)
    app.register_blueprint(notes_module)


def register_login_manager_handlers(app):
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        return redirect(url_for("index"))

    @app.errorhandler(401)
    def unauthorized(e):
        return redirect(url_for("index"))

    @app.errorhandler(404)
    def not_found(e):
        return redirect(url_for("index"))


def register_template_filters(app):
    @app.template_filter('markdown')
    def clean(s):
        return markdown2.markdown(s)

    @app.template_filter('linkify')
    def linkify(s):
        return bleach.linkify(s)


def register_base_routes(app):
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
