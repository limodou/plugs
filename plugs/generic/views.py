#coding=utf-8
from uliweb.i18n import ugettext_lazy as _
from uliweb.orm import get_model
from uliweb import url_for, error, json
from uliweb.utils.common import safe_unicode
from functools import partial

def get_url(suffix, restful=False):
    def _f(action, id=None, suffix=suffix, restful=restful):
        if suffix.endswith('/'):
            suffix = suffix[:-1]
        if action in ('list', 'add'):
            return "%s/%s" % (suffix, action)
        else:
            if restful:
                if action == 'view':
                    return "%s/%s" % (suffix, id)
                return "%s/%s/%s" % (suffix, id, action)
            else:
                return "%s/%s/%s" % (suffix, action, id)
    return _f
    
def generic_list(model=None, get_url=get_url, layout=None, 
    template=None, key_field='id', add_button_text=None, view=None, data=None, 
    json_result=True, pagination=True, rows=10):
    from uliweb.utils.generic import ListView
    from uliweb import request, response
    from uliweb.core.html import Tag
    
    if not view:
        def key(value, obj):
            url = get_url('view', id=obj.id)
            return str(Tag('a', value, href="%s" % url))
       
        if not model or not get_model(model):
            error("Can't find model [%s], please check it" % model)
            
        pageno = int(request.GET.get('pageno', 0))
        rows_per_page=rows
        
        if json_result:
            pageno = int(request.values.get('page', 1)) - 1
            rows_per_page = int(request.values.get('rows', rows))
        fields_convert_map = {key_field:key}
        
        _id = '%s_table' % model
        view =  ListView(model, rows_per_page=rows_per_page, 
            pageno=pageno, id=_id, fields_convert_map=fields_convert_map,
            pagination=pagination)
    else:
        _id = view.id
    
    if 'data' in request.values:
        if json_result:
            return json(view.json())
        else:
            result = view.run(head=False, body=True)
            return json(result)
    else:
        result = view.run(head=True, body=False)
        if isinstance(result, dict):
            layout = layout or 'layout.html'
            template = template or 'generic_list.html'
            response.template = template
            
            data = data or {}
            result['layout'] = layout
            result['table_id'] = _id
            result['get_url'] = get_url
            result['add_button_text'] = add_button_text or _('New')
            if json_result:
                result['table'] = view
            result.update(data)
        return result
    
def generic_add(model=None, get_url=get_url, layout=None, 
    template=None, title=None, view=None, data=None):
    from uliweb.utils.generic import AddView
    from uliweb import response
    
    if not view:
        Model = get_model(model)
        if not model or not Model:
            return error("Can't find model [%s], please check it" % model)

        get_url = partial(get_url, action='view')
        view = AddView(model, get_url)
        
    result = view.run()
    if isinstance(result, dict):
        layout = layout or 'layout.html'
        template = template or 'generic_add.html'
        response.template = template
        if not title:
            name = getattr(model, '__verbose_name__', '')
            title = _("Add") + safe_unicode(name)
        elif callable(title):
            title = title('add')
        data = data or {}
        result['layout'] = layout
        result['get_url'] = get_url
        result['title'] = title
        result.update(data)
    return result
    
def generic_view(model=None, id=None, obj=None, get_url=get_url, layout=None, 
    template=None, title=None, view=None, data=None):
    from uliweb.utils.generic import DetailView
    from uliweb import error, response
    
    if not view:
        Model = get_model(model)
        if not model or not Model:
            return error("Can't find model [%s], please check it" % model)

        if not obj:
            obj = Model.get(Model.c.id == int(id))
        view = DetailView(model, obj=obj)
        
    result = view.run()
    if isinstance(result, dict):
        layout = layout or 'layout.html'
        template = template or 'generic_view.html'
        response.template = template
        if not title:
            name = getattr(model, '__verbose_name__', '')
            title = _("Edit") + safe_unicode(name) + ('(#%d)' % id)
        elif callable(title):
            title = title('view', obj)
        data = data or {}
        result['layout'] = layout
        result['get_url'] = get_url
        result['title'] = title
        result['obj_id'] = id
        result.update(data)
    return result
    
def generic_edit(model=None, id=None, obj=None, get_url=get_url, layout=None, 
    template=None, title=None, view=None, data=None):
    from uliweb.utils.generic import EditView
    from uliweb import response
    
    if not view:
        Model = get_model(model)
        if not model or not Model:
            return error("Can't find model [%s], please check it" % model)

        if not obj:
            obj = Model.get(Model.c.id == int(id))
        view = EditView(model, get_url('view', id=id), obj=obj)
        
    result = view.run()
    if isinstance(result, dict):
        layout = layout or 'layout.html'
        template = template or 'generic_edit.html'
        response.template = template
        if not title:
            name = getattr(model, '__verbose_name__', '')
            title = _("View") + safe_unicode(name) + ('(#%d)' % id)
        elif callable(title):
            title = title('edit', obj)
        data = data or {}
        result['layout'] = layout
        result['get_url'] = get_url
        result['title'] = title
        result['obj_id'] = id
        result.update(data)
    return result
    
def generic_delete(model=None, id=None, obj=None, get_url=get_url, view=None):
    from uliweb.utils.generic import DeleteView
    
    if not view:
        Model = get_model(model)
        if not model or not Model:
            return error("Can't find model [%s], please check it" % model)

        if not obj:
            obj = Model.get(Model.c.id == int(id))
        view = DeleteView(Model, get_url('list'), obj=obj)
        
    return view.run()
    
class View(object):
    model = None
    layout = 'layout.html'
    key_field = 'id'
    add_button_text = _('New')
    pagination = True
    rows = 10
    
    def _get_url(self, action, **kwargs):
        return url_for('.'.join([self.__class__.__module__, 
            self.__class__.__name__, action]), **kwargs)
        
    def _get_title(self, action, obj=None):
        name = getattr(self.model, '__verbose_name__', '')
        if action == 'add':
            return _("Add") + safe_unicode(name)
        elif action == 'edit':
            return _("Edit") + safe_unicode(name)
        elif action == 'view':
            return _("View") + safe_unicode(name)
        
    def _get_template(self, action):
        return 'generic_%s.html' % action
    
    def list(self):
        return generic_list(self.model, layout=self.layout, 
            template=self._get_template('list'),
            get_url=self._get_url, key_field=self.key_field, 
            add_button_text=self.add_button_text, json_result=True,
            rows=self.rows)
            
    def add(self):
        return generic_add(self.model, get_url=self._get_url, layout=self.layout,
            template=self._get_template('add'), title=self._get_title)
            
    def edit(self, id):
        return generic_edit(self.model, id=id, get_url=self._get_url, layout=self.layout,
            template=self._get_template('edit'), title=self._get_title)
    
    def view(self, id):
        return generic_view(self.model, id=id, get_url=self._get_url, layout=self.layout,
            template=self._get_template('view'), title=self._get_title)
        
    def delete(self, id):
        return generic_delete(self.model, id=id, get_url=self._get_url)