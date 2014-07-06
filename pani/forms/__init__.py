from flask.ext.wtf import Form  
from wtforms import BooleanField, TextField, PasswordField, validators, \
        TextAreaField, BooleanField, SelectMultipleField, widgets
from wtfrecaptcha.fields import RecaptchaField

from pani import app

from pani.forms.gvalidators import ValidPassword

from flask_wtf import Form as fwtfForm
from flask_wtf import RecaptchaField

from pani.model.project import Project
from pani.model.user_project import UserProject

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()



class LoginForm(Form):

    username = TextField(
            'Username', 
            [
                validators.Length(min=2, max=20), 
                validators.Required()
            ]
        )
    password = PasswordField(
            'Password', 
            [
                validators.Length(min=6, max=20), 
                validators.Required()
            ]
        )


class DeleteForm(Form):
    pass


class UserForm(Form):

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        if 'user' in kwargs:
            user = kwargs['user']
            kwargs.setdefault('public_key', user.public_key)
            kwargs.setdefault('username', user.username)
            self._user = user
        super(UserForm, self).__init__(formdata, obj, prefix, **kwargs)


    username = TextField(
            'Username', 
            [
                validators.Length(min=2, max=20), 
                validators.Required()
            ]
        )

    password = PasswordField(
            'Password', 
            [
                validators.Length(min=6, max=20), 
                validators.Optional()
            ]
        )



    public_key = TextField(
            'Public Key', 
            [
                validators.Length(min=2, max=30), 
                validators.Optional()
            ]
        )



class ProjectForm(Form):

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        if 'project' in kwargs:
            project = kwargs['project']
            kwargs.setdefault('name', project.name)
            kwargs.setdefault('description', project.description)
            self._project = project
        super(ProjectForm, self).__init__(formdata, obj, prefix, **kwargs)


    name = TextField(
            'Name', 
            [
                validators.Length(min=2, max=20), 
                validators.Required()
            ]
        )


    description = TextField(
            'Description', 
            [
                validators.Length(min=2, max=30), 
                validators.Optional()
            ]
        )



class UserProjectForm(Form):
    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        up = UserProject()
        kwargs.setdefault('projects', up.get_project_ids(kwargs['user_id']))
        super(UserProjectForm, self).__init__(formdata, obj, prefix, **kwargs)


    _choices = Project.get_choices_form()
    projects = MultiCheckboxField(
            label='Projects', 
            choices=_choices,
            coerce=int
        )


