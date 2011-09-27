#coding=utf8
from uliweb.middleware import Middleware
import sys

class TracebackMiddle(Middleware):
    ORDER = 40
    
    def __init__(self, application, settings):
        from uliweb import settings, function

        if settings.GLOBAL.EXCEPTION_PROCESS_TYPE == 'redis':
            self.redis = function('get_redis')()
    
    def process_exception(self, request, e):
        from uliweb import settings
        import traceback
        from uliweb.mail import Mail
        from uliweb.utils.common import Serial
        
        type, value, tb = sys.exc_info()
        txt =  ''.join(traceback.format_exception(type, value, tb))
        
        if settings.GLOBAL.EXCEPTION_PROCESS_TYPE == 'mail':
            Mail().send_mail(settings.get_var('PARA/EMAIL_SENDER'), settings.get_var('PARA/DEV_TEAM'),
                u'Program running error', txt)
        elif settings.GLOBAL.EXCEPTION_PROCESS_TYPE == 'print':
            print txt
        elif settings.GLOBAL.EXCEPTION_PROCESS_TYPE == 'redis':
            mail = {'from':settings.get_var('PARA/EMAIL_SENDER'), 'to':settings.get_var('PARA/DEV_TEAM'),
                'title':u'Program running error', 'message':txt}
            _t = Serial.dump(mail)
            self.redis.lpush('send_mails', _t)
        
        
