from flask import redirect, url_for, request, session, Blueprint, render_template
from .forms import ChangePasswordForm
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from project import db
from project.helpers import Flasher

bp_account = Blueprint('app_account', __name__, url_prefix='/account')


@login_required
@bp_account.route("/change", methods=["POST"])
def change_pass_post():
    form = ChangePasswordForm(request.form)
    if form.validate():
        if check_password_hash(current_user.password, form.password.data) and check_password_hash(
                current_user.random_hashed, session.get('rand_key')):
            current_user.password = generate_password_hash(form.new_password.data)
            current_user.encrypt_rand_key(form.new_password.data, session.get('rand_key'))
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


@login_required
@bp_account.route("/", methods=["GET"])
def change_pass_get():
    form = ChangePasswordForm()
    return render_template("account.html.j2", form=form)
