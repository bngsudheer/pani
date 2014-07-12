# -*- coding: utf-8 -*-
"""
    flask
    ~~~~~

    A mercurial manager. It's a glue application to put together
    various mercurial tools

    :copyright: (c) 2014 by Sudheera Satyanrayana.
    :license: BSD, see LICENSE for more details.
"""

__version__ = '0.1'


from flask import Flask
from flask import request, render_template, flash, session, redirect, url_for

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import current_user



app = Flask(__name__)

app.config.from_envvar('PANI_SITE_SETTINGS')

db = SQLAlchemy(app)

to_import_list = ['default']
temp = __import__('pani.views', globals(), locals(), to_import_list, -1)


from pani.model.user import User

default  = getattr(temp, 'default')
app.add_url_rule('/login', 'login', default.default_login)



login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(userid):
        return User.get_by_id(int(userid))



@app.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    flash('You do not have permission to access the page', 'warning')
    return redirect('/account/login')


ADMINS = ['sudheer@gavika.com']


if __name__ == "__main__":
    app.debug = app.config('DEBUG')
    app.run()


app.secret_key = app.config['SESSION_SECRET_KEY']
