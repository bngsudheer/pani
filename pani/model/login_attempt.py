from collections import namedtuple
from functools import partial
import time

from sqlalchemy.sql import func

from flask.ext.login import current_user

from pani import app
from pani import db

class LoginAttempt(db.Model):

    __tablename__ = 'login_attempts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    ip_address = db.Column(db.String(20), nullable=False)
    success = db.Column(db.Boolean(), nullable=False, default=False)
    date_ = db.Column(db.Integer(), nullable=False, default=time.time())

    def __repr__(self):
        return '<Username %r>' % self.username


    def get_failed_attempts_count(self, ip_address, start_time):
        query = db.session.query(func.count(LoginAttempt.id).label('count')).\
                    filter(LoginAttempt.ip_address == ip_address).\
                    filter(LoginAttempt.date_ > start_time).\
                    filter(LoginAttempt.success == False)


        
        row = query.one()
        return row.count






