from flask.ext.wtf import Form  
from wtforms import BooleanField, TextField, PasswordField, validators, \
        TextAreaField, BooleanField, SelectMultipleField, widgets
from wtfrecaptcha.fields import RecaptchaField

from pani import app

from pani.forms.gvalidators import ValidPassword

from flask_wtf import Form as fwtfForm
from flask_wtf import RecaptchaField



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
                validators.Required()
            ]
        )




