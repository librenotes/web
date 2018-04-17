from project import db

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, default="Untitled")
    content = db.Column(db.Text, default="No content")
    fk_category = db.Column(db.Integer, nullable=True)
    category = db.relationship(Categories)
    isprivate = db.Column(db.Boolean, unique=False, nullable=False, default=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, unique=True)
    hashkey = db.Column(db.Text, unique=False)
    fk_notes = db.Column(db.Integer, db.ForeignKey(Notes.id), nullable=True)
    notes = db.relationship(Notes)

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
