from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Accounts(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return 'id {}, User {}, email {}'.format(self.id, self.username, self.email)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
