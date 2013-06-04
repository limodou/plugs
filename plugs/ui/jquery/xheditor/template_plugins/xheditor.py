def call(app, var, env):
    from uliweb import settings
    
    version = settings.UI_CONFIG.xheditor_version
    lang = settings.UI_CONFIG.xheditor_lang
    a = []
    if version != '1.1.12':
        a.append('xheditor/%s/xheditor-%s.min.js' % (version, version))
        a.append('xheditor/%s/xheditor_lang/%s.js' % (version, lang))
    else:
        a.append('xheditor/%s/xheditor-zh-cn.min.js' % version)
    return {'toplinks':a, 'depends':[('jquery')]}
