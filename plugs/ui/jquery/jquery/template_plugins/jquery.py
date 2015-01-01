def call(version=None, ui=False, theme='redmond', css_only=False):
    from uliweb import settings
    
    a = []
    b = []
    version = version or settings.UI_CONFIG.jquery_version
    ui_version = settings.UI_CONFIG.jquery_ui_version
    if css_only:
        _v = map(int, ui_version.split('.'))
        if _v > [1, 9]:
            return {'toplinks':['jquery/ui/%s/jquery-ui-min.css' % (ui_version, ui_version)]}
        else:
            return {'toplinks':['jquery/ui/%s/css/%s/jquery-ui-%s.custom.css' % (ui_version, theme, ui_version)]}
    if version:
        a.append('jquery/jquery-%s.min.js' % version)
        _v = map(int, version.split('.'))
        if _v > [1, 9]:
            a.append('jquery/jquery-migrate-1.2.1.min.js')
    if ui:
        _v = map(int, ui_version.split('.'))
        if _v > [1, 9]:
            a.append('jquery/ui/%s/jquery-ui.min.css' % ui_version)
            a.append('jquery/ui/%s/jquery-ui.min.js' % ui_version)
            a.append('jquery/ui/%s/jquery.ui.datepicker-zh-CN.min.js' % ui_version)
        else:
            a.append('jquery/ui/%s/css/%s/jquery-ui-%s.custom.css' % (ui_version, theme, ui_version))
            a.append('jquery/ui/%s/jquery-ui.min.js' % ui_version)
            a.append('jquery/ui/%s/js/jquery-ui-%s.custom.min.js' % (ui_version, ui_version))
            a.append('jquery/ui/%s/js/jquery.ui.datepicker.zh.js' % ui_version)
        
    if settings.UI_CONFIG.jquery_bootstrap:
        b.append(settings.UI_CONFIG.jquery_bootstrap)
        
    return {'toplinks':a, 'bottomlinks':b}
