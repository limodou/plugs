#coding=utf-8
from uliweb import expose

def __begin__():
    from uliweb import function
    return function('has_login')()

def get_audit_list(c):
    from uliweb.utils.generic import ListView
    from uliweb.orm import get_model
    from uliweb import request, settings
    from uliweb.utils.textconvert import text2html
    from uliweb.core.js import json_dumps
    
    pageno = int(request.GET.get('pageno', 0))
    
    Audit = get_model('audit')
    condition = None
    order_by = Audit.c.modified_date.desc()
    
    if c.get('table_id'):
        condition = (Audit.c.table_id == c['table_id']) & condition
    if c.get('obj_id'):
        condition = (Audit.c.obj_id == c['obj_id']) & condition
    if c.get('title'):
        condition = (Audit.c.title.like(c['title'])) & condition
    if c.get('modify_flag'):
        condition = (Audit.c.modify_flag == c['modify_flag']) & condition
    if c.get('modified_date'):
        condition = (Audit.c.modified_date == c['modified_date']) & condition
    if c.get('modified_user'):
        condition = (Audit.c.modified_user == c['modified_user']) & condition
    
    def changed_value(value, obj):
        if value:
            import pickle
            return text2html(json_dumps(pickle.loads(value)))
        else:
            return ''
    
    def old_value(value, obj):
        if value:
            import pickle
            return text2html(json_dumps(pickle.loads(value)))
        else:
            return ''

    fields = ({'name':'table_id', 'width':100}, 'obj_id', {'name':'title', 'width':200}, 'modify_flag', 'changed_value', 'old_value',
        'modified_date', 'modified_user')
    
    fields_convert_map = {'changed_value':changed_value, 'old_value':old_value}
    view =  ListView(Audit, condition=condition, order_by=order_by, fields=fields,
        rows_per_page=settings.get_var('PARA/ROWS_PER_PAGE', 10), pageno=pageno, 
        fields_convert_map=fields_convert_map, id='audit_table', pagination=False,
        table_width=False)
        
    return view

@expose('/config/log/list')
def audit_recent():
    from query import create_audit_query
    
    query = create_audit_query(url_for(audit_recent))
    condition = query.run()
    view = get_audit_list(condition)
    if 'data' in request.GET:
        result = view.run(head=False, body=True)
        return json(result)
    else:
        result = view.run(head=True, body=False)
        result.update({'query_form':query.form})
        return result
    