def call(version='1.2.0'):
    from uliweb import settings
    
    version = settings.UI_CONFIG.get('pnotify_version', version)
    a = []
    if map(int, version.split('.')) >= [2, 0, 0]:
        a.append('pnotify/%s/pnotify.custom.min.css' % version)
        a.append('pnotify/%s/pnotify.custom.min.js' % version)
    else:
        a.append('pnotify/%s/jquery.pnotify.default.css' % version)
        a.append('pnotify/%s/jquery.pnotify.default.icons.css' % version)
        a.append('pnotify/%s/jquery.pnotify.min.js' % version)
    return {'toplinks':a}
