from project import db
from werkzeug.security import generate_password_hash, check_password_hash
from Crypto.Cipher import AES
from Crypto import Random
import base64

categories_notes = db.Table(
    'categories_notes',
    db.Column('category_id', db.Integer(), db.ForeignKey('category.id')),
    db.Column('note_id', db.Integer(), db.ForeignKey('note.id'))
)

class AESCipher:
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s : s[:-ord(s[len(s)-1:])]

    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, default="Untitled")
    content = db.Column(db.Text, default="No content")
    isprivate = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    categories = db.relationship(
            'Category',
            secondary=categories_notes,
            backref=db.backref('notes', lazy='dynamic')
        )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text)
    random_hashed = db.Column(db.Text, nullable=False)
    random_encrypted = db.Column(db.Text, nullable=False)
    fk_notes = db.Column(db.Integer, db.ForeignKey(Note.id), nullable=True)
    notes = db.relationship(Note, backref='users')

    def get_random_key(self, plain_pass):
        padded_plain, padded_hashed = self.get_padded_passwords(plain_pass)
        cipher = AES.new(padded_plain, AES.MODE_CBC, padded_hashed)
        rand_key = cipher.decrypt(self.random_encrypted)
        return rand_key

    def get_padded_passwords(self, plain_pass):
        remainder = 16 - len(plain_pass) % 16
        padded_plain = plain_pass + '0' * remainder
        hashed_password = generate_password_hash(plain_pass)
        padded_hashed = hashed_password[-16:]
        return padded_plain, padded_hashed

    def create_rand_key(self, plain_pass):
        rand_key = Random.get_random_bytes(256)
        padded_plain, padded_hashed = self.get_padded_passwords(plain_pass)
        cipher = AES.new(padded_plain, AES.MODE_CBC, padded_hashed)
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
