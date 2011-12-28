def call(app, var, env):
    from uliweb import settings
    
    version = settings.UI_CONFIG.xheditor_version
    a = []
    a.append('xheditor/xheditor-%s-zh-cn.min.js' % version)
    return {'toplinks':a, 'depends':[('jquery')]}
