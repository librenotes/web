from project import db, mailer
from flask import render_template, redirect, url_for, request, Blueprint
from project.models import User
from .forms import RegisterForm
from werkzeug.security import generate_password_hash
from flask_login import current_user
from project.helpers import Flasher, AuthHelper

bp_register = Blueprint('app_register', __name__, url_prefix='/register')


@bp_register.route("/", methods=["GET"])
def register_get():
    if current_user.is_authenticated:
        Flasher.flash("You are already logged in", "success")
        return redirect(url_for('app_notes.notes', username=current_user.username))

    return render_template("register.html.j2", form=RegisterForm())


@bp_register.route("/signup", methods=["POST"])
def register_post():
    form = RegisterForm(request.form)
    if form.validate():
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
            mailer.send_confirmation_mail(form.username.data, form.email.data)
            Flasher.flash("Register Successful, please check your mail address for confirmation", "success")
            return redirect(url_for('app_login.login_get'))
        else:
            Flasher.flash("This username or email address is already in use", "warning")
    else:
        Flasher.flash_errors(form, "danger")
    return redirect(url_for('app_register.register_get'))


@bp_register.route("/confirm", methods=["GET"])
def confirm():
    confirmed = mailer.confirm_token(request.args['token'])
    if confirmed:
        user_ = User.query.filter(User.email == confirmed).first()
        if user_.is_confirmed:
            Flasher.flash("This mail address has been already verified!", "warning")
        else:
            user_.is_confirmed = True
            db.session.commit()
            Flasher.flash("Email verification is successful, now you can login!", "success")
        return redirect(url_for('app_login.login_get'))
    else:
        return "Expired or you are fake"
