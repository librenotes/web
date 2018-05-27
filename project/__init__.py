from flask import Flask, redirect, url_for
from flask_apscheduler import APScheduler
from flask_login import LoginManager
from flask_mail import Mail
from .helpers import Mailer, Flasher, fetch_github_pictures, CommitFeedFetcher
from .models import User, db
import bleach
import markdown2
from flask_caching import Cache

login_manager = LoginManager()

mail = Mail()
mailer = Mailer()
cache = Cache()
feed_fetcher = CommitFeedFetcher()


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
    feed_fetcher.init_cache(cache)
    scheduler = APScheduler()
    scheduler.init_app(app)
    setup_scheduled_jobs(scheduler=scheduler)
    scheduler.start()
    # setup and start scheduled jobs
    # Registers
    register_blueprints(app)
    register_error_handlers(app)
    # register_base_routes(app)
    register_template_filters(app)
    register_login_manager_handlers()
    return app


def setup_scheduled_jobs(scheduler):
    # setup github image fetchers that fetches up to date profile pictures of us to put on about us part
    fetch_list = [('ozanonurtek', 'https://avatars3.githubusercontent.com/u/14114739?s=100&v=4'),
                  ('vrct', 'https://avatars3.githubusercontent.com/u/16005747?s=100&v=4'),
                  ('shubidubapp', 'https://avatars0.githubusercontent.com/u/16193640?s=100&v=4')]
    i = 0
    for i in range(len(fetch_list)):
        name, url = fetch_list[i]
        kwargs = dict(url=url,
                      path="project/static/img/github_{}.jpeg".format(name))
        fetch_github_pictures(**kwargs)
        scheduler.add_job(id=str(i), name='{}_github'.format(name), func=fetch_github_pictures,
                          kwargs=kwargs,
                          trigger='interval', days=7)

    # add the job that refreshes librenotes repos github commit history
    i += 1
    scheduler.add_job(id=str(i), name='feed_fetcher', func=feed_fetcher.update, trigger='interval', minutes=15)
    feed_fetcher.update()


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
