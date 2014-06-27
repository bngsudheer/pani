import hashlib
import time

from sqlalchemy import or_

from flask.ext.mail import Message
from flask import request, render_template, flash, session, redirect, url_for, \
    current_app, abort
from flask.ext.login import login_user
from flask.ext.login import login_required
from flask.ext.login import current_user
from flask.ext.login import logout_user
from flask.ext.principal import Principal, Identity, AnonymousIdentity, \
    identity_changed
from flask.ext.principal import identity_loaded, RoleNeed, UserNeed
from flask.ext.principal import Permission as FPermission

from pani import app
from pani import db
from pani import mail

from pani.forms import LoginForm

from pani.model.user import User




@app.route('/account')
@login_required
def account_index():

    return render_template('/account/index.html', user=current_user)


@app.route("/account/login", methods=["GET", "POST"])
def account_login():
    form = LoginForm()
    message = ''
    if form.validate_on_submit():
        hash_ = hashlib.sha512()
        hash_.update(form.password.data)
        password = hash_.hexdigest()
        user = User.query.filter_by(password=password).\
                filter_by(username=form.username.data).\
                first()
        if user:
            # login and validate the user...
            login_user(user)
            # Tell Flask-Principal the identity changed
            identity_changed.send(
                    current_app._get_current_object(), 
                    identity=Identity(user.id)
                )
            flash("Logged in successfully")
            return redirect('/account')
        else:
            message = 'Invalid username or password'
    return render_template("/account/login.html", form=form, message=message)

@app.route('/account/logout')
@login_required
def account_logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
                session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                                      identity=AnonymousIdentity())

    flash("Logged out successfully")
    return redirect(request.args.get('next') or '/')



@app.route("/account/unauthorized", methods=["GET"])
def account_unauthorized():
    return 'unauthorized to access this page'





