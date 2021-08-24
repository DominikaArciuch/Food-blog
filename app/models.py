from app import db


class Accounts(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return 'id {}, User {}, email {}'.format(self.id, self.username, self.email)