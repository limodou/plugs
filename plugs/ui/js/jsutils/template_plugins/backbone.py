def call(app, var, env, version=None):
    from uliweb import settings
    
    version = version or settings.UI_CONFIG.backbone_version
    a = []
    a.append('jsutils/backbone-%s.min.js' % version)
    return {'bottomlinks':a, 'depends':['jquery', 'underscore']}
