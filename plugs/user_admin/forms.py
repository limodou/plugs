#coding=utf-8
from uliweb.form import *
from uliweb.i18n import ugettext as _

class ChangeInfoForm(Form):
    form_buttons = Button(value=_('Save'), _class="btn btn-primary", type="submit")
    form_title = _('Change Basic Information')

    email = StringField(label=_('Email:'))
    image = ImageField(label=_('Portrait:'))
    action = HiddenField(default='changeinfo')
    
class ChangePasswordForm1(Form):
    form_buttons = Button(value=_('Save'), _class="btn btn-primary", type="submit")

    oldpassword = PasswordField(label=_('Old Password:'), required=True)
    password = PasswordField(label=_('Password:'), required=True)
    password1 = PasswordField(label=_('Password again:'), required=True)

    def form_validate(self, all_data):
        from uliweb import request
        error = {}
        
        if not request.user.check_password(all_data.oldpassword):
            error['oldpassword'] = _('Password is not right.')

        if all_data.password != all_data.password1:
            error['password1'] = _('Passwords are not the same between two types.')
        
        return error
    
class ChangePasswordForm2(Form):
    form_buttons = Button(value=_('Save'), _class="btn btn-primary", type="submit")

    username = StringField(label=_('Username:'), required=True)
    oldpassword = PasswordField(label=_('Old Password:'), required=True)
    password = PasswordField(label=_('Password:'), required=True)
    password1 = PasswordField(label=_('Password again:'), required=True)
    
    def form_validate(self, all_data):
        from uliweb.orm import get_model
        error = {}
        
        User = get_model('user')
        user = User.get(User.c.username == data)
        if not user:
            raise ValidationError, _('Username is not existed.')
        
        if not request.user.check_password(all_data.oldpassword):
            error['oldpassword'] = _('Password is not right.')

        if all_data.password != all_data.password1:
            error['password1'] = _('Passwords are not the same between two types.')
            
        return error
import re

r_username = re.compile(r'[a-zA-Z0-9\._/]')

class AddUserForm(Form):
    def validate_username(self, data):
        from uliweb.orm import get_model
        
        if any((x in data for x in '<>& ')):
            return _("Username can't include illegal characters, such as '<>&' and blank.")

        if not r_username.match(data):
            return _("Username can only include letter, number and '._/'.")

        User = get_model('user')
        user = User.get(User.c.username == data)
        if user:
            return _('The username is already existed!')
    
class EditUserForm(Form):
    def validate_username(self, data):
        from uliweb.orm import get_model
                 
        if any((x in data for x in '<>& ')):
            return _("Username can't include illegal characters, such as '<>&' and blank.")
        
        if not r_username.match(data):
            return _("Username can only include letter, number and '._/'.")
        
        User = get_model('user')
        user = User.get((User.c.username == data) & (User.c.id != self.object.id))
        if user:
            return _('Username is already existed.')

class UploadImageForm(Form):
    pass