def call(version=None):
    from uliweb import settings

    version = version or settings.UI_CONFIG.select2_version
    a = []
    if version[0] == '3':
        a.append('select2/%s/select2.css' % version)
        a.append('select2/%s/select2.js' % version)
    elif version[0] == '4':
        a.append('select2/%s/css/select2.css' % version)
        a.append('select2/%s/js/select2.js' % version)

    return {'toplinks':a, 'depends':['jquery']}
