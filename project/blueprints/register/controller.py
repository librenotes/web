from project import db
from flask import render_template, redirect, url_for, request, Blueprint
from project.models import User
from .forms import RegisterForm
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user
from project.blueprints import Flasher, AuthHelper

bp_register = Blueprint('app_register', __name__, url_prefix='/register')


@bp_register.route("/", methods=["GET"])
def register_get():
    if AuthHelper.check_authentication(current_user):
        Flasher.flash("You are already logged in", "success")
        return redirect(url_for('app_notes.notes', username=current_user.username))

    return render_template("register.html.j2", form=RegisterForm())


@bp_register.route("/signup", methods=["POST"])
def register_post():
    form = RegisterForm(request.form)
    if AuthHelper.check_form_validation(form):
        if not AuthHelper.check_user_exist(form.email.data, form.username.data):
            # Create new user
            user = User()
            user.username = form.username.data
            user.password = generate_password_hash(form.password.data)
            user.email = form.email.data
            user.generate_encryption_keys(form.password.data)
            # Add to db
            db.session.add(user)
            db.session.commit()
            # Login new user
            login_user(user)
            AuthHelper.set_random_key(user, form.password.data)
            Flasher.flash("Register Successful, now you are logged in!", "success")
            return redirect(url_for('app_notes.notes', username=user.username))
        else:
            Flasher.flash_errors("This username or email address is already in use", "warning")
    else:
        Flasher.flash_errors(form, "danger")
    return redirect(url_for('app_register.register_get'))
