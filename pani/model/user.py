from collections import namedtuple
from functools import partial

from flask.ext.login import current_user

from pani import app
from pani import db

class User(db.Model):

    __tablename__ = 'users'

    sqlite_autoincrement=True

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128), default=None)
    public_key = db.Column(db.String(500))

    def __repr__(self):
        return '<User %r>' % self.username


    @classmethod
    def get_by_id(cls, id_):
        id_ = int(id_)
        user = User.query.filter_by(id=id_).first()
        return user


    def get_id(self):
        return unicode(self.id)
            
            
    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    

    def is_anonymous(self):
        return False
