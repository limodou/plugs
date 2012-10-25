def call(app, var, env, version=None, ui=False, theme='redmond', css_only=False):
    from uliweb import settings
    
    a = []
    b = []
    version = version or settings.UI_CONFIG.jquery_version
    ui_version = settings.UI_CONFIG.jquery_ui_version
    if css_only:
        return {'toplinks':['jquery/ui/css/%s/jquery-ui-%s.custom.css' % (theme, ui_version)]}
    if version:
        a.append('jquery/jquery-%s.min.js' % version)
    if ui:
        a.append('jquery/ui/css/%s/jquery-ui-%s.custom.css' % (theme, ui_version))
        a.append('jquery/jquery-%s.min.js' % version)
        a.append('jquery/ui/js/jquery-ui-%s.custom.min.js' % ui_version)
        a.append('jquery/ui/js/jquery.ui.datepicker.zh.js')
        
    if settings.UI_CONFIG.jquery_bootstrap:
        b.append(settings.UI_CONFIG.jquery_bootstrap)
        
    return {'toplinks':a, 'bottomlinks':b}
