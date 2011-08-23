#coding=utf-8
from uliweb.core.SimpleFrame import expose, url_for
from uliweb.contrib.auth.views import login

def login():
    from uliweb.contrib.auth import authenticate, login
    from forms import LoginForm
    from uliweb.form import Submit, Tag
    
    LoginForm.form_buttons = [Submit(value=_('Login'), _class="button")]
    
    form = LoginForm()
    
    if request.method == 'GET':
        form.next.data = request.GET.get('next', '/')
        return {'form':form, 'message':''}
    if request.method == 'POST':
        flag = form.validate(request.params)
        if flag:
            f, d = authenticate(request, username=form.username.data, password=form.password.data)
            if f:
                request.session.remember = form.rememberme.data
                login(request, form.username.data)
                next = request.POST.get('next', '/')
                return redirect(next)
            else:
                data = d
        m = form.errors.get('_', '') or 'Login failed!'
        flash(m, 'error')
        return {'form':form}


