from project import db

categories_notes = db.Table(
    'categories_notes',
    db.Column('category_id', db.Integer(), db.ForeignKey('category.id')),
    db.Column('note_id', db.Integer(), db.ForeignKey('note.id'))
)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, default="Untitled")
    content = db.Column(db.Text, default="No content")
    fk_category = db.Column(db.Integer, nullable=True)
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
    password = db.Column(db.Text, unique=True)
    random_md5 = db.Column(db.Text, unique=True, nullable=False)
    random_encrypted = db.Column(db.Text, unique=True, nullable=False)
    fk_notes = db.Column(db.Integer, db.ForeignKey(Note.id), nullable=True)
    notes = db.relationship(Note, backref='users')


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
