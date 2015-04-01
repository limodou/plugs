def call(version=None, components=None):
    '''
    components param example:
        components={"checkbox":["js","css"],"api":"js","image":"css"}
    '''
    from uliweb import settings

    a = []
    version = version or settings.UI_CONFIG.semanticui_version
    a.append('semantic/%s/semantic.js' % (version))
    if settings.UI_CONFIG.google_fonts_mirror:
        a.append('semantic/%s/semantic_%s.css' % (version,settings.UI_CONFIG.google_fonts_mirror))
    else:
        a.append('semantic/%s/semantic.css' % (version))
    if components and isinstance(components,dict):
        for k in components:
            ext = components[k]
            if isinstance(ext,(str,unicode)):
                a.append('semantic/%s/components/%s.%s' % (version,k,ext))
            elif isinstance(ext,list):
                for e in ext:
                    a.append('semantic/%s/components/%s.%s' % (version,k,e))
    return {'toplinks':a, 'depends':['jquery']}
