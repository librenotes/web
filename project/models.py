from project import db
from werkzeug.security import generate_password_hash, pbkdf2_bin
from .aesCipher import AESCipher
from os import urandom


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, default="Untitled")
    content = db.Column(db.Text, default="No content")
    isprivate = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    categories = db.Column(db.Text, unique=False, default="#nocategory")
    user = db.relationship("Note")

    def decrypt(self, rand_key):
        cipher = AESCipher(rand_key)
        if self.isprivate:
            self.title = cipher.decrypt(self.title)
            self.content = cipher.decrypt(self.content)
            self.categories = cipher.decrypt(self.categories)

    def encrypt(self, rand_key):
        cipher = AESCipher(rand_key)
        if self.isprivate:
            self.title = cipher.encrypt(self.title)
            self.content = cipher.encrypt(self.content)
            self.categories = cipher.encrypt(self.categories)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    salt = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text)
    random_hashed = db.Column(db.Text, nullable=False)
    random_encrypted = db.Column(db.Text, nullable=False)
    fk_notes = db.Column(db.Integer, db.ForeignKey(Note.id), nullable=True)
    notes = db.relationship(Note)

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

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __str__(self):
        return self.username
