from flask import Flask
from flask import request, render_template, flash, session, redirect, url_for

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import current_user



app = Flask(__name__)

app.config.from_envvar('MAILADMIN_SITE_FLASK_SETTINGS')

db = SQLAlchemy(app)
mail = Mail(app)

to_import_list = ['account', 'default', 'user']
temp = __import__('pani.views', globals(), locals(), to_import_list, -1)


from pani.model.user import User

account = getattr(temp, 'account')
default  = getattr(temp, 'default')
app.add_url_rule('/account/login', 'login', account.account_login)



login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(userid):
        return User.get_by_id(int(userid))


@identity_loaded.connect_via(app)
def post_login(sender, identity):
     # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))


@app.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    flash('You do not have permission to access the page', 'warning')
    return redirect('/account/login')


ADMINS = ['sudheer@gavika.com']

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'service@gavika.com',
                               ADMINS, 'Mailadmin Error')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


if __name__ == "__main__":
    app.debug = app.config('DEBUG')
    app.run()


app.secret_key = app.config['SESSION_SECRET_KEY']
