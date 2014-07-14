def call(version=None):
    from uliweb import settings
    
    version = version or settings.UI_CONFIG.underscore_version
    a = []
    a.append('jsutils/underscore-%s.min.js' % version)
    return {'bottomlinks':a}
