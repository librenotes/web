from flask import render_template, redirect, url_for, request, Blueprint
from project.models import User
from .forms import LoginForm
from flask_login import current_user, login_user
from project.blueprints import Flasher, AuthHelper

bp_login = Blueprint('app_login', __name__, url_prefix='/login')


@bp_login.route("/", methods=["GET"])
def login_get():
    if current_user.is_authenticated:
        Flasher.flash("You are already logged in", "success")
        return redirect(url_for('app_notes.notes', username=current_user.username))
    else:
        return render_template("login.html.j2", form=LoginForm())


@bp_login.route("/signin", methods=["POST"])
def login_post():
    form = LoginForm(request.form)
    if form.validate():
        user_ = User.query.filter_by(username=form.username.data).first()
        if user_ and AuthHelper.check_password(user_, form.password.data):
            login_user(user_)
            AuthHelper.set_random_key(user_.get_random_key(form.password.data))
            Flasher.flash("Login Successful!", category="success")
            return redirect(url_for('app_notes.notes', username=form.username.data))
        else:
            Flasher.flash("Password or Username does not match", "danger")
            return redirect(url_for("app_login.login_get"))
    else:
        Flasher.flash_errors(form, "danger")
        return redirect(url_for("app_login.login_get"))
