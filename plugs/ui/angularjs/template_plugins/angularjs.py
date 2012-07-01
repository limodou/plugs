def call(app, var, env, version=None):
    from uliweb import settings
    
    a = []
    version = version or settings.UI_CONFIG.angularjs_version
    a.append('angularjs/%s/angular-%s.min.js' % (version, version))
    return {'toplinks':a}