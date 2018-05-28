from flask import redirect, url_for, request, Blueprint, render_template
from .forms import ChangePasswordForm, ChangeDescription
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_required
from project import db
from project.helpers import Flasher, AuthHelper

bp_account = Blueprint('app_account', __name__, url_prefix='/account')


@bp_account.route("/change", methods=["POST"])
@login_required
def change_pass_post():
    form = ChangePasswordForm(request.form)
    if form.validate():
        if AuthHelper.check_password(current_user, form.password.data) and AuthHelper.check_session_validation(
                current_user):
            current_user.password = generate_password_hash(form.new_password.data)
            current_user.encrypt_rand_key(form.new_password.data, AuthHelper.get_random_key())
            db.session.commit()
            Flasher.flash("Your password is successfully changed", "success")
            return redirect(url_for("app_notes.notes", username=current_user.username))
        else:
            Flasher.flash("Your current password doesn't match with entered password or you are fake!",
                          category='warning')
            return redirect(url_for("app_notes.notes", username=current_user.username))
    else:
        Flasher.flash_errors(form)
        return redirect(url_for("app_notes.notes", username=current_user.username))


@bp_account.route("/", methods=["GET"])
@login_required
def change_pass_get():
    return render_template("account.html.j2", form=ChangePasswordForm(), description_form=ChangeDescription())


@bp_account.route("/changedescription", methods=["POST"])
@login_required
def change_description_post():
    form = ChangeDescription(request.form)
    if form.validate():
        if AuthHelper.check_session_validation(current_user):
            current_user.description = form.description.data
            db.session.commit()
            Flasher.flash("Your description is successfully changed", "success")
        else:
            Flasher.flash("Are you fake?",
                          category='warning')
    else:
        Flasher.flash_errors(form)
    return redirect(url_for("app_notes.notes", username=current_user.username))
