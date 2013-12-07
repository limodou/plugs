#coding=utf8

from uliweb import functions
from uliweb.form import *

class WikiEdit(Form):
    form_buttons = [Button(value=_('Save'), _class="btn btn-primary", type='submit'),
        '<a href="javascript:history.back();" class="btn">取消</a>']
    
    name = UnicodeField(label='页面名称', required=True)
    subject = UnicodeField(label='页面显示名称')
    content = TextField(label='内容', rows=15, required=True, datatype=unicode)
    slug = HiddenField()
    
    def form_validate(self, all_data):
        import re
        
        error = {}
        
        if not re.match(ur'^[\u4e00-\u9fa5_a-zA-Z0-9]+$', all_data['name'], re.U):
            error['name'] = u'页面名称只能为汉字，英文字母，数字或_'
            
        #检查页面名称是否已经存在
        Wiki = functions.get_model('wikipage')
        if self.parent:
            pagename = self.parent + '/' + all_data['name']
        else:
            pagename = all_data['name']
        wiki = Wiki.get((Wiki.c.name==pagename) & (Wiki.c.id!=self.wiki.id) & (Wiki.c.enabled==True) & (Wiki.c.deleted==False))
        if wiki:
            error['name'] = u'已经存在同名的页面，请换一个名字或者去同名页面进行修改'
        return error
    
class WikiAclForm(Form):
    form_buttons = [Button(value='测试', _class="btn btn-primary", type='button', id='btnTest')]

    acl = TextField(label='权限描述串', html_attrs={'style':'width:80%'})
    username = UnicodeField(label='用户登录名')