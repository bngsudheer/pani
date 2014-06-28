import wtforms
from wtforms import ValidationError
import hashlib


class ValidPassword(object):
    """
    Check if user's password is correct 
    """
    def __init__(self, user=None, message=None):
        self.message = message

    def __call__(self, form, field):
        hash_ = hashlib.sha512()
        hash_.update(form.password.data)
        password = hash_.hexdigest()

        if password != form._user.password:
            if self.message is None:
                self.message = field.gettext(u'Invalid password')
            raise wtforms.ValidationError(self.message)





