from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_mail import Mail
from .helpers import Mailer, Flasher
from .models import User, db
import bleach
import markdown2
from flask_caching import Cache

login_manager = LoginManager()

mail = Mail()
mailer = Mailer()
cache = Cache()


def create_app(config):
    # Init app
    app = Flask(__name__)
    app.config.from_object(config)
    # Init extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    mailer.init_app(app, mail)
    cache.init_app(app)
    # Registers
    register_blueprints(app)
    register_error_handlers(app)
    # register_base_routes(app)
    register_template_filters(app)
    register_login_manager_handlers()
    return app


def register_blueprints(app):
    from project.blueprints.login.controller import bp_login as login_module
    from project.blueprints.register.controller import bp_register as register_module
    from project.blueprints.notes.controller import bp_notes as notes_module
    from project.blueprints.index.controller import bp_index as index_module
    from project.blueprints.account.controller import bp_account as account_module
    app.register_blueprint(login_module)
    app.register_blueprint(register_module)
    app.register_blueprint(notes_module)
    app.register_blueprint(index_module)
    app.register_blueprint(account_module)


def register_login_manager_handlers():
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        return redirect(url_for("app_index.index"))

    @app.errorhandler(401)
    def unauthorized(e):
        return redirect(url_for("app_index.index"))

    @app.errorhandler(404)
    def not_found(e):
        return redirect(url_for("app_index.index"))


def register_template_filters(app):
    @app.template_filter('markdown')
    def clean(s):
        return markdown2.markdown(s)

    @app.template_filter('linkify')
    def linkify(s):
        return bleach.linkify(s)

