import hashlib

from flask import render_template
from flask import request, render_template, flash, session, redirect, url_for

from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import current_user

from flask.ext.paginate import Pagination

from pani import app
from pani.forms import LoginForm
from pani.forms import UserForm

from pani.model.user import User
from pani import db

@app.route('/')
@login_required
def default_index():
    """Default index view.
    """
    return render_template('/index.html', show_big_header=True)


@app.route('/account')
@login_required
def account_index():

    return render_template('/account/index.html', user=current_user)


@app.route("/login", methods=["GET", "POST"])
def default_login():
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
            flash("Logged in successfully")
            return redirect('/account')
        else:
            message = 'Invalid username or password'
    return render_template("/account/login.html", form=form, message=message)


@app.route("/edit_user", methods=["GET", "POST"])
def default_edit_user():
    user = User.get_by_id(int(request.args.get('user_id')))
    form = UserForm(request.form, user=user)
    message = ''
    if form.validate_on_submit():
        flash("Edited")
        return redirect('/account')
    return render_template("/edit_user.html", form=form, message=message)



@app.route('/logout')
@login_required
def account_logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
                session.pop(key, None)


    flash("Logged out successfully")
    return redirect(request.args.get('next') or '/')



@app.route("/account/unauthorized", methods=["GET"])
def account_unauthorized():
    return 'unauthorized to access this page'




@app.route('/users')
@login_required
def user_index():

    page = int(request.args.get('page', 1))
    per_page = 10

    users = db.session.query(User)
    total_users = users.count()
    users = users.offset(per_page*(page-1))

    users = users.limit(per_page)
    
    pagination = Pagination(
            page=page, 
            total=total_users, 
            search=False, 
            record_name='users', 
            bs_version='3'
        )

    return render_template(
            '/account/users.html', 
            users=users, 
            pagination=pagination
        )


@app.route('/user/add', methods=["GET", "POST"])
@login_required
def user_add():
    form = UserForm(request.form)
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data

        if form.password.data:

            hash_ = hashlib.sha512()
            hash_.update(form.password.data)
            password = hash_.hexdigest()

            user.password = password
        else:
            user.password = None
 
        user.public_key = form.public_key.data

        db.session.add(user)
        db.session.commit()
        flash("User has been added successfully")
        return redirect('/users')
      
    return render_template(
            '/add_user.html', 
            form=form,
            logged_in=False,
        )


@app.route('/account/edit_user')
@login_required
def edit_index():
    pass




