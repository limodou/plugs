def call(app, var, env, version='1.2.0'):
    from uliweb import settings
    
    version = settings.UI_CONFIG.get('pnotify_version', '')
    if version:
        version += '/'
    a = []
    a.append('pnotify/%sjquery.pnotify.default.css' % version)
    a.append('pnotify/%sjquery.pnotify.default.icons.css' % version)
    a.append('pnotify/%sjquery.pnotify.min.js' % version)
    return {'toplinks':a}
