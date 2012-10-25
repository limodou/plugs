def call(app, var, env, plugins=None, js=True, responsive=False, version=None):
    from uliweb import settings
    
    plugins = plugins or []
    a = []
    version = version or settings.UI_CONFIG.bootstrap_version
    a.append('<!--[if lt IE 9]>')
    a.append('bootstrap/asset/html5.js')
    a.append('<![endif]-->')
    a.append('bootstrap/%s/bootstrap.min.css' % version)
    if responsive or settings.UI_CONFIG.bootstrap_responsive:
        a.append('bootstrap/%s/bootstrap-responsive.min.css' % version)
    
    jquery = False
    jquery_ui = False
    for x in plugins:
        a.append('bootstrap/%s/js/bootstrap-%s.js' % (version, x))
        jquery = True
        if x in ['pagination']:
            jquery_ui = True
            
    if js:
        jquery = True
        a.append('bootstrap/%s/js/bootstrap.min.js' % version)
      
    d = {'toplinks':a, 'depends':[]}
    if jquery:
        d['depends'] = [('jquery', {'ui':jquery_ui}), 'json2']
    return d
