def call(app, var, env, plugins=None):
    plugins = plugins or []
    a = []
    a.append('<!--[if lt IE 9]>')
    a.append('bootstrap/asset/html5.js')
    a.append('<![endif]-->')
    a.append('bootstrap/bootstrap.min.css')
    
    jquery = False
    for x in plugins:
        a.append('bootstrap/js/bootstrap-%s.js' % x)
        jquery = True
      
    d = {'toplinks':a}
    if jquery:
        d['depends'] = ['jquery']
    return d
