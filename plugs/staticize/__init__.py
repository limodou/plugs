import os
from uliweb import UliwebError, functions
from uliweb.utils.common import log, safe_str
from hashlib import md5

class Backend(object):
    def get_key(self, key):
        return md5(safe_str(key)).hexdigest()
    
    def get(self, key, creator=None, update=False):
        raise NotImplementedError
    
    def delete(self, key):
        raise NotImplementedError
    
class FileBackend(Backend):
    def __init__(self, path_to, subdir=''):
        self.path_to = path_to
        self.subdir = subdir
        
    def get(self, key, creator=None, update=False):
        _file = os.path.join(self.path_to, self.subdir, self.get_key(key))
        if update or not os.path.exists(_file):
            txt = creator()
            
            #create path_to directory first
            dir = os.path.dirname(_file)
            if not os.path.exists(dir):
                os.makedirs(dir)
                
            #write the content
            with open(_file, 'wb') as f:
                f.write(txt)
        else:
            with open(_file) as f:
                txt = f.read()
        return txt
    
    def delete(self, key):
        _file = os.path.join(self.path_to, self.subdir, self.get_key(key))
        if os.path.exists(_file):
            try:
                os.remove(_file)
            except:
                log.exception()
            
class RedisBackend(Backend):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        
    def get(self, key, creator=None, update=False):
        redis = functions.get_redis(**self.kwargs)
        txt = ''
        if not update:
            txt = redis.get(self.get_key(key))
        if update or not txt:
            txt = creator()
            redis.set(self.get_key(key), txt)
        
        return txt
    
    def delete(self, key):
        redis = functions.get_redis(**self.kwargs)
        redis.delete(self.get_key(key))
        
_types = {'file':FileBackend, 'redis':RedisBackend}
def get_staticize(backend=None, **kwargs):
    from uliweb import settings
    
    type = settings.get_var('STATICIZE/backend', 'file')
    _cls = _types.get(type)
    if not _cls:
        raise UliwebError("Can't found staticize type %s, please check the spell." % type)
    kw = settings.get_var('STATICIZE_BACKENDS/%s' % type, {})
    kw.update(kwargs)
    handler = _cls(**kw)
    return handler
    
