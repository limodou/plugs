def call(app, var, env, version=None, all=True):
    from uliweb import settings
    
    version = version or settings.UI_CONFIG.blockui_version
    a = []
    if version == "2.46":
        a.append('blockui/%s/jquery.blockUI.js' % (version))
    
    return {'toplinks':a, 'depends':['jquery']}
