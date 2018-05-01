from flask import render_template, redirect, url_for, request, session, flash, Blueprint
from project.models import User
from .forms import LoginForm
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash

bp_login = Blueprint('app_login', __name__, url_prefix='/login')


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), category='danger')


@bp_login.route("/", methods=["GET"])
def login_get():
    if current_user.is_authenticated:
        flash("You are already logged in", "success")
        return redirect(url_for('app_notes.notes', username=current_user.username))
    else:
        form = LoginForm()
        return render_template("login.html.j2", form=form)


@bp_login.route("/signin", methods=["POST"])
def login_post():
    form = LoginForm(request.form)
    if form.validate():
        user_ = User.query.filter_by(username=form.username.data).first()
        if user_ and check_password_hash(user_.password, form.password.data):
            login_user(user_)
            session['rand_key'] = user_.get_random_key(form.password.data)
            flash('Login Successful!', category='success')
            return redirect(url_for('app_notes.notes', username=form.username.data))
        else:
            flash('Password or Username does not match', category='danger')
            return redirect(url_for("app_login.login_get"))
    else:
        flash_errors(form)
        return redirect(url_for("app_login.login_get"))
