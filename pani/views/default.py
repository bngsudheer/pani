import hashlib

from flask import render_template
from flask import request, render_template, flash, session, redirect, url_for

from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import current_user

from flask.ext.paginate import Pagination

from pani import app
from pani.forms import LoginForm
from pani.forms import UserForm
from pani.forms import ProjectForm
from pani.forms import UserProjectForm
from pani.forms import DeleteForm

from pani.model.user import User
from pani.model.project import Project
from pani.model.user_project import UserProject

from pani import db

@app.route('/')
@login_required
def default_index():
    """Default index view."""
    return render_template('/index.html', show_big_header=True)


@app.route('/account')
@login_required
def default_account():
    """My Account view."""
    return render_template('/account.html', user=current_user)


@app.route("/login", methods=["GET", "POST"])
def default_login():
    """View with login form."""
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
    return render_template("/login.html", form=form, message=message)


@app.route("/edit_user", methods=["GET", "POST"])
def default_edit_user():
    """View to edit the user."""
    user = User.get_by_id(int(request.args.get('user_id')))
    form = UserForm(request.form, user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        if form.password.data:
            hash_ = hashlib.sha512()
            hash_.update(form.password.data)
            password = hash_.hexdigest()
            user.password = password
        if form.public_key.data:
            user.public_key = form.public_key.data

        db.session.commit()
        flash("User has been edited successfully")
        return redirect('/users')
    return render_template("/edit_user.html", form=form, user=user)

@app.route("/edit_project", methods=["GET", "POST"])
def default_edit_project():
    """View to list the projects of the user."""
    project = Project.get_by_id(int(request.args.get('project_id')))
    form = ProjectForm(request.form, project=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        db.session.commit()
        flash("Project has been successfully edited")
        return redirect('/projects')
    return render_template("/edit_project.html", form=form, project=project)



@app.route('/logout')
@login_required
def default_logout():
    """Logout the user."""
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
                session.pop(key, None)


    flash("Logged out successfully")
    return redirect(request.args.get('next') or '/')



@app.route("/unauthorized", methods=["GET"])
def default_unauthorized():
    """View for unauthorized access of the application."""
    return 'unauthorized to access this page'


@app.route('/users')
@login_required
def default_users():
    """View to list the users."""
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
            '/users.html', 
            users=users, 
            pagination=pagination
        )


@app.route('/projects')
@login_required
def default_projects():
    """View to list the projects."""
    page = int(request.args.get('page', 1))
    per_page = 10

    projects = db.session.query(Project)
    total_projects = projects.count()
    projects = projects.offset(per_page*(page-1))

    projects = projects.limit(per_page)
    
    pagination = Pagination(
            page=page, 
            total=total_projects, 
            search=False, 
            record_name='projects', 
            bs_version='3'
        )

    return render_template(
            '/projects.html', 
            projects=projects, 
            pagination=pagination
        )


@app.route('/user/add', methods=["GET", "POST"])
@login_required
def default_user_add():
    """Form to add a user account."""
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


@app.route('/add_project', methods=["GET", "POST"])
@login_required
def default_add_project():
    """Add a project."""
    form = ProjectForm(request.form)
    if form.validate_on_submit():
        project = Project()
        project.name = form.name.data
        project.description = form.description.data

        db.session.add(project)
        db.session.commit()
        flash("Project has been added successfully")
        return redirect('/projects')
      
    return render_template(
            '/add_project.html', 
            form=form,
        )


@app.route('/user_projects', methods=["GET", "POST"])
@login_required
def default_user_projects():
    """List the projects of the user."""
    user_id = int(request.args.get('user_id'))

    form = UserProjectForm(request.form, user_id=user_id) 
    if request.method == 'POST' and form.validate():
        query = db.session.query(UserProject).\
                filter(UserProject.user_id==user_id)
        query = query.delete()

        for project_id in form.projects.data:
            up = UserProject()
            up.user_id = user_id
            up.project_id = project_id
            db.session.add(up)

        db.session.commit()
        flash('The user\'s projects have been saved.', 'message')
        return redirect('/user_projects?user_id=%s'%user_id)

    return render_template(
            '/user_projects.html', 
            form=form,
            user_id=user_id,
        )


@app.route('/save_settings', methods=["GET", "POST"])
@login_required
def default_save_settings():
    """Generate the .ssh/authorized_keys file"""

    form = DeleteForm(request.form) 

    if form.validate_on_submit():

        authorize_keys_file = open(app.config['AUTHORIZED_KEYS_PATH'], 'w')
        lines = ""

        for user in db.session.query(User):
            print "###############3"
            print user.username
            print lines
            user_projects = UserProject().get_projects(user.id)
            projects = ""
            for user_project in user_projects:
                if projects:
                    projects = "%s %s"%(projects, user_project.name)
                else:
                    # For the first line no need to add any spaces
                    projects = "%s"%(user_project.name)

            projects = projects.strip()

            line = "command=\"cd /home/mercurial/repositories && hg-ssh %s \" %s"%(projects, user.public_key)
            if lines:
                lines = "%s\n%s"%(lines, line)
            else:
                # For the first line, no need to append any spaces or newlines
                lines = "%s"%(line)

            print lines
        lines = lines.strip()
        authorize_keys_file.write(lines)
        authorize_keys_file.close()
        flash('The settings have been saved to file')
        return redirect('/')

       

    return render_template(
            '/save_settings.html', 
            form=form,
        )




