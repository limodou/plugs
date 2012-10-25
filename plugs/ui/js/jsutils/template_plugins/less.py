def call(app, var, env, version=None):
    from uliweb import settings
    
    version = version or settings.UI_CONFIG.less_version
    a = []
    a.append('jsutils/less-%s.min.js' % version)
    return {'bottomlinks':a}
