def call(plugins=None, version=None, iframe_transport=False):
    from uliweb import settings
    a = []
    version = version or settings.UI_CONFIG.jqupload_version
    if version == "default":
        a.append('jqupload/%s/jquery.iframe-transport.js'%(version))
        a.append('jqupload/%s/jquery.fileupload.js'%(version))
    else:
        a.append('jqupload/%s/js/jquery.iframe-transport.js'%(version))
        a.append('jqupload/%s/js/jquery.fileupload.js'%(version))

        plugins = plugins or []
        for x in plugins:
            a.append('bootstrap/%s/js/jquery.fileupload-%s.js' % (version, x))

        a.append('jqupload/%s/css/jquery.fileupload.css'%(version))
    return {'toplinks':a, 'depends':[('jquery', {'ui':True})]}
