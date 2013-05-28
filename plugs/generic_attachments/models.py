#coding=utf8
from uliweb.orm import *
from uliweb.i18n import ugettext_lazy as _
from uliweb.utils.generic import GenericReference

class Generic_Attachment(Model):
    filepath = Field(FILE, verbose_name=_('Filepath'))
    filename  = Field(str, verbose_name=_('Filename'), max_length=255)
    content_object = GenericReference(verbose_name=_('Related Object'))
    submitter = Reference('user', verbose_name=_('Submitter'))
    created_date = Field(datetime.datetime, verbose_name=_('Created Date'), auto_now_add=True)
    enabled = Field(bool, verbose_name=_('Enabled Flag'))
    deleted = Field(bool, verbose_name=_('Deleted Flag'))
    slug = Field(str, verbose_name=_('Slug'), max_length=32) 
