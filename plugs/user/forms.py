#coding=utf-8
from uliweb.form import *
from uliweb.i18n import ugettext as _

class LoginForm(Form):
    form_buttons = Submit(value=_('Login'), _class="button")
    form_title = _('Login')
    
    username = UnicodeField(label=_('Username:'), required=True)
    password = PasswordField(label=_('Password:'), required=True)
    rememberme = BooleanField(label=_('Remember Me'))
    next = HiddenField()
    
    def form_validate(self, all_data):
        from uliweb import settings
        from uliweb.orm import get_model
        
        User = get_model('user')
        user = User.get(User.c.username==all_data['username'])
        if not user:
            return {'username': _('User "%s" does not exist!') % all_data['username']}
        if not user.check_password(all_data['password']):
            return {'password' : _('Password is not right.')}
        
