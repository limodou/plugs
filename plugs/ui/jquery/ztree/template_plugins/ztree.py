def call(app, var, env, plugins=None, version=None, all=True):
    from uliweb import settings
    
    plugins = plugins or []
    a = []
    version = version or settings.UI_CONFIG.ztree_version
    if version == '2.6':
        a.append('ztree/%s/style/zTreeStyle.css' % version)
        a.append('ztree/%s/style/zTreeIcons.css' % version)
        a.append('ztree/%s/jquery.ztree-%s.min.js' % (version, version))
    elif version == '3.0':
        a.append('ztree/%s/style/zTreeStyle.css' % version)
        a.append('ztree/%s/jquery.ztree.core-%s.min.js' % (version, version))
        for p in plugins:
            a.append('ztree/%s/jquery.ztree.%s-%s.min.js' % (version, p, version))
    elif version == '3.1':
        a.append('ztree/%s/css/zTreeStyle.css' % version)
        if all:
            a.append('ztree/%s/jquery.ztree.all-3.1.min.js' % version)
        else:
            a.append('ztree/%s/jquery.ztree.core-%s.min.js' % (version, version))
            for p in plugins:
                a.append('ztree/%s/jquery.ztree.%s-%s.min.js' % (version, p, version))
        
    return {'toplinks':a, 'depends':['jquery']}
