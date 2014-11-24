def call(plugins=None, version=None):
    from uliweb import settings

    plugins = plugins or []
    a = []
    version = version or settings.UI_CONFIG.bootstrap_version
    a.append('<!--[if lt IE 9]>')
    a.append('bootstrap/asset/html5.js')
    a.append('<![endif]-->')
    _v = map(int, version.split('.'))
    if _v > [2, 3]:
        a.append('bootstrap/%s/css/bootstrap.min.css' % version)
#       a.append('bootstrap/%s/css/bootstrap-responsive.min.css' % version)
    else:
        a.append('bootstrap/%s/bootstrap.min.css' % version)
#       a.append('bootstrap/%s/bootstrap-responsive.min.css' % version)

    for x in plugins:
        a.append('bootstrap/%s/js/bootstrap-%s.js' % (version, x))

    a.append('bootstrap/%s/js/bootstrap.min.js' % version)

    d = {'toplinks':a, 'depends':[]}
    d['depends'] = ['jquery', 'json2']
    return d
