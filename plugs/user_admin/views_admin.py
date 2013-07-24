#coding=utf-8
from __future__ import with_statement

from uliweb import expose, decorators, functions
import plugs.generic.views as g_views

get_url = g_views.get_url('/users')

def _get_portrait_image_filename(id):
    import os
    return os.path.join('portraits', str(id) + '.tmp' + '.jpg')

def _get_portrait_image_thumbnail(id, size=50):
    import os
    return os.path.join('portraits', str(id) + '.%dx%d' % (size, size) + '.jpg')
    
@expose('/user')
class UserView(object):
    @decorators.require_login
    def view(self):
        return UsersManageView().view(request.user.id)

    @decorators.require_login
    def edit(self):
        from uliweb.utils.generic import EditView
        
        view = EditView('user', condition=request.user.id, ok_url=url_for(UserView.view))
        return view.run()
    
    @decorators.require_login
    def edit_image(self):
        from forms import UploadImageForm
        from uliweb.utils.generic import EditView
        import os
        from PIL import Image
        
        def pre_save(obj, data):
            if 'image' in data and data['image']:
                data['image'].filename = _get_portrait_image_filename(request.user.id)
                
        image = _get_portrait_image_filename(request.user.id)
        f = functions.get_filename(image)
        if os.path.exists(f):
            url = functions.get_href(image)
            img = Image.open(f)
            template_data = {'image_url':url, 'size':img.size}
        else:
            url = None
            template_data = {'image_url':url, 'size':(0, 0)}
            
        view = EditView('user', condition=request.user.id, ok_url=url_for(UserView.edit_image),
            pre_save=pre_save, fields=['image'], template_data=template_data, file_convert=False)
        
        return view.run()
    
    @decorators.require_login
    def save_image(self):
        from uliweb.utils.image import crop_resize
        from uliweb.contrib.upload import get_filename
        
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        
        of = get_filename(_get_portrait_image_filename(request.user.id))
        f = get_filename(_get_portrait_image_thumbnail(request.user.id, size=50))
        crop_resize(of, f, x, y, w, h, size=(50, 50))
        f = get_filename(_get_portrait_image_thumbnail(request.user.id, size=20))
        crop_resize(of, f, x, y, w, h, size=(20, 20))
        flash(_('Save portrait successful'))
        return redirect(url_for(UserView.view))
    
    def change_password(self):
        from uliweb.orm import get_model
        
        User = get_model('user')
        user_id = request.GET.get('user_id', None)
        data = {}
        if user_id:
            user = User.get(int(user_id))
            if user:
                data = {'username':user.username}
        from forms import ChangePasswordForm1, ChangePasswordForm2
        if request.user:
            form = ChangePasswordForm1()
        else:
            form = ChangePasswordForm2(data=data)
        if request.method == 'GET':
            return {'form':form, 'ok':False}
        if request.method == 'POST':
            flag = form.validate(request.POST)
            if flag:
                User = get_model('user')
                if user_id:
                    user = User.get(User.c.username == form.username.data)
                    user.set_password(form.password.data)
                    flash(_('Password saved successfully.'))
                    return redirect('/login?next=/')
                else:
                    request.user.set_password(form.password.data)
                    flash(_('Password saved successfully.'))
                    return {'form':form, 'ok':True}
            else:
                if '_' in form.errors:
                    message = form.errors['_']
                else:
                    message = _('There are something wrong, please fix them.')
                flash(message, 'error')
                return {'form':form, 'ok':False}
    
#def get_users_list_view(c):
#    from uliweb.utils.generic import ListView
#    from uliweb.orm import get_model
#    from uliweb import request
#    from uliweb.core.html import Tag
#    from uliweb import orm
#    
#    def username(value, obj):
#        return str(Tag('a', value, href='/users/%d' % obj.id))
#    
#    def boolean_convert(b, obj):
#        if b:
#            return '<div class="ui-icon ui-icon-check"></div>'
#        else:
#            return '<div class="ui-icon ui-icon-closethick"></div>'
#    
#    pageno = int(request.GET.get('pageno', 0))
#    
#    User = get_model('user')
#    query = None
#    condition = None
#    if c.get('username'):
#        condition = (User.c.username.like(c['username'])) & condition
#    
#    fields_convert_map = {'username':username}
#    
#    fields = [
#        {'name':'username'},
#        {'name':'email', 'width':120},
#        {'name':'is_superuser', 'width':80},
#        {'name':'date_join', 'width':'120'},
#        {'name':'last_login', 'width':'120'},
#    ]
#    
#    view =  ListView(User, condition=condition, query=query, fields=fields,
#        rows_per_page=settings.get_var('PARA/ROWS_PER_PAGE', 10), pageno=pageno, 
#        fields_convert_map=fields_convert_map, id='users_table')
#    view.types_convert_map = {orm.BooleanProperty:boolean_convert}
#    return view
#
@expose('/users')
class UsersManageView(object):
    def __begin__(self):
        from uliweb import function
        return function('require_login')()
        
    def _get_users_list_view(self, c):
        from uliweb.utils.generic import ListView
        from uliweb.orm import get_model
        from uliweb import request
        from uliweb.core.html import Tag
        from uliweb import orm
        
        def username(value, obj):
            return str(Tag('a', value, href='/users/view/%d' % obj.id))
        
        def boolean_convert(b, obj):
            if b:
                return '<div class="ui-icon ui-icon-check"></div>'
            else:
                return '<div class="ui-icon ui-icon-closethick"></div>'
        
        pageno = int(request.values.get('page', 1)) - 1
        rows_per_page = int(request.values.get('rows', settings.get_var('PARA/ROWS_PER_PAGE', 10)))
        
        User = get_model('user')
        query = None
        condition = None
        if c.get('username'):
            condition = (User.c.username.like('%'+c['username']+'%')) & condition
        
#        fields = [
#            {'name':'username'},
#            {'name':'email', 'width':150},
#            {'name':'is_superuser', 'width':80},
#            {'name':'date_join', 'width':150},
#            {'name':'last_login', 'width':150},
#        ]
        
        fields_convert_map = {'username':username}
        view =  ListView(User, condition=condition, query=query, 
#            fields=fields,
            rows_per_page=rows_per_page, pageno=pageno, 
            fields_convert_map=fields_convert_map, id='users_table')
        view.types_convert_map = {orm.BooleanProperty:boolean_convert}
        return view
    
    def _create_user_query(self, url):
        from uliweb.utils.generic import QueryView
        
        fields = ('username',) 
        query = QueryView('user', ok_url=url, fields=fields)
        return query
    
    def list(self):
        query_view = self._create_user_query(url_for(UsersManageView.list))
        c = query_view.run()

        view = self._get_users_list_view(c)
        if 'data' in request.GET:
            result = view.run(head=False, body=True)
            return json(view.json())
        else:
            result = view.run(head=True, body=False)
            result.update({'query_form':query_view.form, 'table':view})
            return result
    
    def add(self):
        from uliweb.utils.generic import AddView
        from uliweb.orm import get_model
        from forms import AddUserForm
        from functools import partial
        
        
        def post_save(obj, data):
            obj.set_password(settings.USER_ADMIN.DEFAULT_PASSWORD)
            
        if request.user.is_superuser:
            view = AddView('user', partial(get_url, 'view'), 
            post_save=post_save, form_cls=AddUserForm)
            return view.run()
        else:
            flash(_('You have no previlege to create user.'), 'error')
            return redirect(url_for(config_users_list))
    
    def view(self, id):
        from uliweb.utils.generic import DetailView
        from uliweb import orm
        from uliweb.contrib.upload import get_filename, get_url
        import os
        
        User = orm.get_model('user')
        
        def boolean_convert(b, obj):
            if b:
                return '<div class="ui-icon ui-icon-check"></div>'
            else:
                return '<div class="ui-icon ui-icon-closethick"></div>'
        
        user = User.get(int(id))
        if not user:
            error(_('User is not exists!'))
            
        image = functions.get_filename(_get_portrait_image_thumbnail(user.id))
        if os.path.exists(image):
            image_url = functions.get_href(_get_portrait_image_thumbnail(user.id))
        else:
            image_url = user.get_image_url()
        can_modify = user.id == request.user.id
        template_data = {'image_url':image_url, 'can_modify':can_modify}
        view = DetailView('user', obj=user, template_data=template_data, table_class_attr='table table-bordered')
        view.types_convert_map = {orm.BooleanProperty:boolean_convert}
        return view.run()
    
    def edit(self, id):
        from uliweb.utils.generic import EditView
        from forms import EditUserForm

        if request.user.is_superuser:
            view = EditView('user', condition=int(id), ok_url=get_url('view', id=id),
                form_cls=EditUserForm, meta='AdminEditForm')
            return view.run()
        else:
            flash(_('You have no previlege to edit user.'), 'error')
            return redirect(request.referrer)
    
    def delete(self, id):
        from uliweb.utils.generic import DeleteView
        
        if request.user.is_superuser:
            view = DeleteView('user', condition=int(id), ok_url=get_url('list'))
            return view.run()
        else:
            flash(_('You have no previlege to delete user.'), 'error')
            return redirect(url_for(users_view, id=id))
    
    def _reset(id):
        from uliweb.orm import get_model
        
        User = get_model('user')
        if request.user.is_superuser:
            user = User.get(int(id))
            user.set_password(settings.PARA.DEFAULT_PASSWORD)
            flash(_('Password reset successfully.'))
            return redirect(request.referrer)
        else:
            flash(_('You have no previlege to reset user password.'), 'error')
            return redirect(url_for(users_view, id=id))
            
@expose('/resign')
def resign():
    from uliweb.contrib.auth import logout
    logout()
    return redirect(url_for('login', next=request.referrer or '/'))

@expose('/users/search')
def users_search():
    from uliweb.orm import get_model
    
    User = get_model('user')
    v_field = request.values.get('label', 'title')
    if request.values.get('term'):
        result = []
        name = request.values.get('term')
        for x in User.filter(User.c.username.like('%'+name+'%') | User.c.nickname.like('%'+name+'%')).limit(functions.get_var('USER_ADMIN/SEARCH_USERS_LIMIT')):
            if x.nickname:
                title = x.nickname+'('+x.username+')'
            else:
                title = x.username
            result.append({'id':x.id, v_field:title})
        return json(result)
    else:
        return json([])
            
