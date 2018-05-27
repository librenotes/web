from project import db
from flask import render_template, request, session, abort, Blueprint, flash, redirect, url_for
from flask_login import current_user, login_required
from .forms import NoteForm, DeleteNoteForm
from project.models import User, Note, Category
# from werkzeug.security import check_password_hash
# from re import split
from project.helpers import NoteHelper, AuthHelper, CategoryHelper

bp_notes = Blueprint('app_notes', __name__, url_prefix='/notes')


@bp_notes.route("/<username>/")
@bp_notes.route("/<username>")
def notes(username):
    if current_user.is_authenticated and AuthHelper.check_username(current_user, username) \
            and AuthHelper.check_session_validation(current_user):
        note_list = NoteHelper.get_user_notes(current_user)
        return render_template("notes.html.j2", notes=note_list, edit_form=NoteForm(), delete_form=DeleteNoteForm(),
                               title="{} @ Librenotes".format(username),
                               description="Welcome, {}".format(username))
    else:
        note_list, searched_user = NoteHelper.get_searched_user_notes(username)
        if searched_user:
            flash("You are seeing public notes of {}".format(username), "warning")
            description = "See public notes of {}".format(username)
            if searched_user.description is not None:
                description = searched_user.description
            return render_template("notes.html.j2", notes=note_list, edit_form=None, delete_form=None,
                                   title="{} @ Librenotes".format(username),
                                   description=description)
        else:
            abort(404)


@bp_notes.route("/operation/edit", methods=["POST"])
@login_required
def edit_note():
    form = NoteForm(request.form)
    note = NoteHelper.get_user_note_with_id(current_user, form.id.data)
    if note and form.validate() and AuthHelper.check_session_validation(current_user):
        # Update note
        note.title = form.title.data
        note.content = form.content.data
        note.isprivate = form.isprivate.data
        # Update note categoires
        splitted_list = CategoryHelper.split_and_filter(form.categories.data, '')
        new_categories = CategoryHelper.get_new_categories(splitted_list, note.isprivate)
        # Delete categories of note
        note.categories = []
        # Append it
        current_user.categories.extend(new_categories)
        note.categories.extend(new_categories)
        note.encrypt(AuthHelper.get_random_key())
        db.session.commit()
        return redirect(url_for('app_notes.notes', username=current_user))
    else:
        return abort(404)


@bp_notes.route("/operation/new", methods=["POST"])
@login_required
def add_note():
    form = NoteForm(request.form)
    if AuthHelper.check_session_validation(current_user) and form.validate():
        # Create new note
        note = Note()
        note.title = form.title.data
        note.content = form.content.data
        note.isprivate = form.isprivate.data
        # Get categories
        splitted_list = CategoryHelper.split_and_filter(form.categories.data, '')
        print(splitted_list)
        new_categories = CategoryHelper.get_new_categories(splitted_list, note.isprivate)
        print(new_categories)
        # Relations
        current_user.categories.extend(new_categories)
        note.categories.extend(new_categories)
        # Encrypt
        note.encrypt(AuthHelper.get_random_key())
        # Database operations
        db.session.add(note)
        current_user.notes.append(note)
        db.session.commit()
        return redirect(url_for('app_notes.notes', username=current_user.username))
    else:
        abort(404)


@bp_notes.route("/operation/delete", methods=["POST"])
@login_required
def delete_note():
    form = DeleteNoteForm(request.form)
    note = NoteHelper.get_user_note_with_id(current_user, form.id.data)
    if note and AuthHelper.check_session_validation(current_user):
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for('app_notes.notes', username=current_user.username))
    else:
        return abort(404)

# @bp_notes.route("/new_test", methods=['GET'])
# @login_required
# def new():
#     user_ = current_user
#     user_ = User.query.filter_by(id=user_.id).first()
#     if check_password_hash(user_.random_hashed, session.get("rand_key")):
#         for i in range(10):
#             note = Note()
#             note.title = "This is the {}. note's title".format(i)
#             note.content = "And this is the content of {}".format(i)
#             note.isprivate = True if i % 2 == 0 else False
#             db.session.add(note)
#             categories = split(r' ?#', "#And #we #have #crazy #categories #{}".format(i).lower())
#             categories.remove('')
#             if not note.isprivate:
#                 categories.append('public')
#             for category_name in categories:
#                 if note.isprivate:
#                     category = Category(name=category_name, isprivate=note.isprivate)
#                 else:
#                     category = Category.query.filter_by(name=category_name).first()
#                     if category is None:
#                         category = Category(name=category_name, isprivate=note.isprivate)
#                 db.session.add(category)
#                 category.notes.append(note)
#                 category.users.append(user_)
#             note.encrypt(session.get("rand_key"))
#             user_.notes.append(note)
#         db.session.commit()
#         return 'OK'
#     else:
#         return "YOU ARE FAKE!!!"
#
#
# def user_categories(username):
#     user_ = current_user
#     categories = []
#     if user_.is_authenticated and user_.username == username and check_password_hash(user_.random_hashed,
#                                                                                      session.get("rand_key")):
#         rand_key = session.get("rand_key")
#         for category in user_.categories:
#             category_name = category.decrypt(rand_key)
#             categories.append(category_name)
#     else:
#         searched_user = User.query.filter_by(username=username)
#         if searched_user:
#             categories = Category.query.filter_by(isprivate=False).filter(
#                 Category.users.any(User.id == searched_user.id)).all()
#     return categories
#
#
# @bp_notes.route("/<username>/<category_name>")
# def filter_cat(username, category_name):
#     user_ = current_user
#     category_name = category_name.lower().strip()
#     edit_form = NoteForm()
#     delete_form = DeleteNoteForm()
#     notes = []
#
#     if user_.is_authenticated and user_.username == username and check_password_hash(user_.random_hashed,
#                                                                                      session.get("rand_key")):
#         rand_key = session.get("rand_key")
#         for category in user_.categories:
#             decrypted_name = category.decrypt(rand_key)
#             print(decrypted_name)
#             print(category_name)
#             if decrypted_name == category_name:
#                 notes_ = Note.query.order_by(Note.updated_on.desc()).filter_by(user=user_).filter(
#                     Note.categories.any(Category.id == category.id)).all()
#                 for note in notes_:
#                     note_ = note.decrypt(rand_key)
#                     notes.append(note_)
#         return render_template("notes.html.j2", notes=notes, edit_form=edit_form, delete_form=delete_form)
#
#     else:
#         searched_user = User.query.filter_by(username=username).first()
#         if searched_user is not None:
#             for note in Note.query.filter_by(isprivate=False, user=searched_user).filter(
#                     Note.categories.any(Category.name == category_name)).order_by(Note.updated_on.desc()).all():
#                 note_ = note.decrypt(session.get("rand_key"))
#                 notes.append(note_)
#             return render_template("notes.html.j2", notes=notes, edit_form=None, delete_form=None)
#
#         else:
#             abort(404)
