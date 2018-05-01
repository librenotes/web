from project import db
from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from project.models import User
from .forms import RegisterForm
from werkzeug.security import generate_password_hash
from flask_login import  login_user

bp_register = Blueprint('app_register', __name__, url_prefix='/register')


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), category='danger')


@bp_register.route("/", methods=["GET"])
def register_get():
    form = RegisterForm()
    return render_template("register.html.j2", form=form)


@bp_register.route("/signup", methods=["POST"])
def register_post():
    form = RegisterForm(request.form)
    if form.validate():
        user_ = User.query.filter_by(username=form.username.data).first()
        email_ = User.query.filter_by(email=form.email.data).first()
        if not (user_ or email_):  # check if username or email address already exists.
            user = User()
            user.username = form.username.data
            user.password = generate_password_hash(form.password.data)
            user.email = form.email.data
            user.generate_encryption_keys(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            session['rand_key'] = user.get_random_key(form.password.data)
            flash('Register Successful, now you are logged in!', category='success')
            return redirect(url_for('app_notes.notes', username=form.username.data))
        else:
            flash('This username or email address is already in use', category='warning')
    else:
        flash_errors(form)
    return redirect(url_for('app_register.register_get'))
