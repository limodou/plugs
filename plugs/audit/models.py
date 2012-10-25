#coding=utf-8

from uliweb.orm import *
from uliweb.utils.common import get_var
import datetime
from uliweb.i18n import gettext_lazy as _

class Audit(Model):
    table_id = Reference('tables', verbose_name=_('OperationTable'), required=True)
    title = Field(str, max_length=255, verbose_name=_('Title'))
    obj_id = Field(int, verbose_name="ID", required=True)
    changed_value = Field(BLOB, verbose_name=_('ModifiedContent'))
    old_value = Field(BLOB, verbose_name=_('OriginalContent'))
    modify_flag = Field(CHAR, max_length=1, verbose_name=_('ModifiedFlag'), choices=get_var('PARA/AUDIT_MODIFY_FLAG'))
    modified_date = Field(datetime.datetime, verbose_name=_('ModifiedDate'))
    modified_user = Reference('user', verbose_name=_('ModifiedUser'), collection_name='modifier_audits')
    
