#coding=utf-8

from uliweb.orm import *
from uliweb.utils.common import get_var
from uliweb.i18n import ugettext_lazy as _

class Message(Model):
    __verbose_name__ = _(u'Message')
    
    type =  Field(CHAR, verbose_name=_('Message Type'), max_length=1, choices=get_var('MESSAGES/MESSAGE_TYPE'))
    message = Field(TEXT, verbose_name=_('Content'))
    user = Reference('user', verbose_name=_('User'), collection_name='user_messages')
    read_flag = Field(bool, verbose_name=_('Read Flag'))
    create_date = Field(datetime.datetime, verbose_name=_('Create Time'), auto_now=True, auto_now_add=True)
    sender = Reference('user', verbose_name=_('Sender'))
    send_flag = Field(CHAR, max_length=1, verbose_name=_('Send Flag'), default='r') #'s' 发送， 'r' 接收

    def __unicode__(self):
        return self.message
    
    class Table:
        fields = [
            'message',
            'type',
            'user',
            'read_flag',
            'create_date',
            'sender',
            'id',
            'send_flag',
            'user_image',
        ]
    
    @classmethod
    def OnInit(cls):
        Index('msg_idx', cls.c.user, cls.c.read_flag)
    