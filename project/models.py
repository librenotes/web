from werkzeug.security import generate_password_hash, pbkdf2_bin
from .cipher import AESCipher
from os import urandom
from sqlalchemy import func
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

category_note = db.Table('Category_Note',
                         db.Column('category_id', db.Integer, db.ForeignKey('Category.id')),
                         db.Column('note_id', db.Integer, db.ForeignKey('Note.id'))
                         )

category_user = db.Table('Category_User',
                         db.Column('category_id', db.Integer, db.ForeignKey('Category.id')),
                         db.Column('user_id', db.Integer, db.ForeignKey('User.id')))


class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    salt = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text)
    random_hashed = db.Column(db.Text, nullable=False)
    random_encrypted = db.Column(db.Text, nullable=False)
    notes = db.relationship('Note')
    categories = db.relationship('Category', secondary=category_user,
                                 lazy='joined', backref=db.backref('users', lazy='joined'))
    is_confirmed = db.Column(db.Boolean, default=False)

    def __init__(self): pass

    def generate_encryption_keys(self, plain_pass):
        self.__generate_salt()
        self.__generate_random_key(plain_pass)

    def __generate_salt(self):
        self.salt = urandom(16)

    def __get_hashed_pass(self, plain_pass):
        return pbkdf2_bin(plain_pass, salt=self.salt, keylen=32)

    def get_random_key(self, plain_pass):
        hashed_pass = self.__get_hashed_pass(plain_pass)
        cipher = AESCipher(hashed_pass)
        rand_key = cipher.decrypt(self.random_encrypted)
        return rand_key

    def __generate_random_key(self, plain_pass):
        rand_key = urandom(16)
        hashed_pass = self.__get_hashed_pass(plain_pass)
        cipher = AESCipher(hashed_pass)
        random_encrypted = cipher.encrypt(rand_key)
        self.random_encrypted = random_encrypted
        self.random_hashed = generate_password_hash(rand_key)

    def __str__(self):
        return self.username

    def encrypt_rand_key(self, plain_pass, rand_key):
        hashed_pass = self.__get_hashed_pass(plain_pass)
        cipher = AESCipher(hashed_pass)
        random_encrypted = cipher.encrypt(rand_key)
        self.random_encrypted = random_encrypted
        self.random_hashed = generate_password_hash(rand_key)


class Note(db.Model):
    __tablename__ = "Note"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, default="Untitled")
    content = db.Column(db.Text, default="No content")
    isprivate = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    categories = db.relationship('Category', secondary=category_note,
                                 lazy='joined', backref=db.backref('notes', lazy='joined'))
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def decrypt(self, rand_key):
        cipher = AESCipher(rand_key)
        note_ = NoteRepresenter()
        note_.id = self.id
        if self.isprivate:
            note_.title = cipher.decrypt(self.title).decode("utf-8")
            note_.content = cipher.decrypt(self.content).decode("utf-8")
        else:
            note_.title = self.title
            note_.content = self.content

        note_.isprivate = self.isprivate
        note_.user = self.user
        for category in self.categories:
            note_.categories.append(category.decrypt(rand_key))

        return note_

    def encrypt(self, rand_key):
        cipher = AESCipher(rand_key)
        if self.isprivate:
            self.title = cipher.encrypt(self.title)
            self.content = cipher.encrypt(self.content)
            for category in self.categories:
                category.encrypt(rand_key)


@db.event.listens_for(Note.categories, 'remove')
@db.event.listens_for(Note.categories, 'append')
def updated_on(target, value, initiator):
    target.updated_on = func.now()


class NoteRepresenter(object):
    def __init__(self):
        self.id = 0
        self.title = ""
        self.content = ""
        self.isprivate = True
        self.user = User
        self.categories = []


class Category(db.Model):
    __tablename__ = "Category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    isprivate = db.Column(db.Boolean, default=True)

    def encrypt(self, rand_key):
        cipher = AESCipher(rand_key)
        if self.isprivate:
            self.name = cipher.encrypt(self.name)
        return self

    def decrypt(self, rand_key):
        if self.isprivate:
            cipher = AESCipher(rand_key)
            return cipher.decrypt(self.name).decode("utf-8")
        else:
            return self.name

    def __repr__(self):
        return "Category(id={}, name={}, isprivate={}".format(self.id, self.name, self.isprivate)


class ContactMessage(db.Model):
    __tablename__ = "ContactMessage"
    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.Text, nullable=False)
    sender_mail = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
