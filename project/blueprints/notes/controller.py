from project import db
from flask import render_template, request, session, abort, Blueprint
from flask_login import current_user, login_required
from .forms import NoteForm, DeleteNoteForm
from project.models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash

bp_notes = Blueprint('app_notes', __name__, url_prefix='/notes')

@bp_notes.route("/<username>")
def notes(username):
    edit_form = NoteForm()
    delete_form = DeleteNoteForm()
    user_ = current_user
    notes = []
    if user_.is_authenticated and user_.username == username and check_password_hash(user_.random_hashed, session.get("rand_key")):
        for note in Note.query.filter_by(user=user_).all():
            note.decrypt(session.get("rand_key"))
            notes.append(note)
        return render_template("notes.html.j2", notes=notes, edit_form=edit_form, delete_form=delete_form)
    else:
        searched_user = User.query.filter_by(username=username).first()
        if searched_user is not None:
            notes =  Note.query.filter_by(user=searched_user, isprivate=False).all()
            return render_template("notes.html.j2", notes=notes, edit_form = edit_form, delete_form= delete_form)

    abort(404)

@bp_notes.route("/operation/edit", methods=["POST"])
@login_required
def edit_note():
    form = NoteForm(request.form)
    user_ = current_user
    print(form.content.data)
    print(type(form.isprivate.data))
    note = Note.query.filter_by(user=user_, id=form.id.data).first()
    if note and check_password_hash(user_.random_hashed, session.get("rand_key")):
        note.decrypt(session.get("rand_key"))
        note.title = form.title.data
        note.content = form.content.data
        note.categories = form.categories.data
        note.isprivate = form.isprivate.data
        note.encrypt(session.get("rand_key"))
        db.session.commit()
        return str(200)
    return str(500)


@bp_notes.route("/operation/new", methods=["POST"])
@login_required
def add_note():
    form = NoteForm(request.form)
    user_ = current_user
    if check_password_hash(user_.random_hashed, session.get("rand_key")):
        note = Note()
        note.title = form.title.data
        note.content = form.content.data
        note.categories = form.categories.data
        note.isprivate = form.isprivate.data
        note.encrypt(session.get("rand_key"))
        db.session.add(note)
        user_.notes.append(note)
        db.session.commit()
        return str(200)
    return str(500)


@bp_notes.route("/operation/delete", methods=["POST"])
@login_required
def delete_note():
    form = DeleteNoteForm(request.form)
    user_ = current_user
    note = Note.query.filter_by(user=user_, id=form.id.data).first()
    if note and check_password_hash(user_.random_hashed, session.get("rand_key")):
        db.session.delete(note)
        db.session.commit()
        return str(200)
    return str(500)

# @app.route("/new_test", methods=['GET'])
# @login_required
# def new():
#     user_ = current_user
#     user_ = User.query.filter_by(id=user_.id).first()
#     print(user_.notes)
#     if check_password_hash(user_.random_hashed, session.get("rand_key")):
#         for i in range(10):
#             note = Note()
#             note.title = "This is the {}. note's title".format(i)
#             note.content = "And this is the content of {}".format(i)
#             note.categories = "#And #we #have #crazy #categories #{}".format(i)
#             note.isprivate = True if i % 2 == 0 else False
#             note.encrypt(session.get("rand_key"))
#             db.session.add(note)
#             user_.notes.append(note)
#         db.session.commit()
#         return 'OK'
#     else:
#         return "FUCK MY ASS"
#
#
# @app.route("/dbc")
# def createdb():
#     db.drop_all()
#     db.create_all()
#     return "OK"
