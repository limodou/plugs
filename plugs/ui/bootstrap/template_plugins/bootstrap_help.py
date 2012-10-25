def call(app, var, env, version=None):
    from uliweb import settings
    
    version = version or settings.UI_CONFIG.bootstrap_version
    a = ['bootstrap/%s/bootstrap.help.js' % version]
    return {'toplinks':a, 'depends':['bootstrap']}
