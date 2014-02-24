#coding=utf-8

from uliweb.orm import *
from uliweb.utils.common import get_var
import datetime
from uliweb.i18n import gettext_lazy as _

class Audit(Model):
    __dispatch_enabled__ = False

    table_id = Reference('tables', verbose_name=_('OperationTable'), required=True)
    title = Field(str, max_length=255, verbose_name=_('Title'))
    obj_id = Field(int, verbose_name="ID", required=True)
    changed_value = Field(BLOB, verbose_name=_('ModifiedContent'))
    old_value = Field(BLOB, verbose_name=_('OriginalContent'))
    modify_flag = Field(CHAR, max_length=1, verbose_name="修改标志", choices=get_var('PARA/AUDIT_MODIFY_FLAG'))
    modified_date = Field(datetime.datetime, verbose_name='修改时间', index=True)
    modified_user = Reference('user', verbose_name='修改人', collection_name='modifier_audits')
    user_info = Field(str, max_length=255, verbose_name='其他信息')
    url = Field(str, max_length=255,verbose_name='访问链接')
    
    class Table:
        fields = [
            {'name':'table_id', 'width':100}, 
            {'name':'obj_id', 'width':40},
            {'name':'modify_flag', 'width':60},
            {'name':'changed_value', 'width':300}, 
            {'name':'old_value', 'width':300},
            'modified_date', 
            'modified_user',
            {'name':'title', 'width':200}, 
            {'name':'url','width':200},
            {'name':'user_info', 'width':200},
        ]
    
    @classmethod
    def OnInit(cls):
        Index('audit_idx', cls.c.table_id, cls.c.obj_id)
