from collections import namedtuple
from functools import partial

from flask.ext.login import current_user

from pani import app
from pani import db


class Project(db.Model):

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(128), default=None)

    def __repr__(self):
        return '<Project %r>' % self.name

    @classmethod
    def get_by_id(cls, id_):
        id_ = int(id_)
        project = cls.query.filter_by(id=id_).first()
        return project

    @classmethod
    def get_choices_form(cls):

        projects = db.session.query(cls)
        items = []
        for project in projects:
            items.append((project.id, project.name))

        return items
