def call(app, var, env, version='1.7', ui=False, theme='redmond', css_only=False):
    a = []
    ui_version = '1.8.16'
    if css_only:
        return {'toplinks':['jquery/ui/css/%s/jquery-ui-%s.custom.css' % (theme, ui_version)]}
    if version:
        a.append('jquery/jquery-%s.js' % version)
    if ui:
        a.append('jquery/ui/css/%s/jquery-ui-%s.custom.css' % (theme, ui_version))
        a.append('jquery/jquery-%s.js' % version)
        a.append('jquery/ui/js/jquery-ui-%s.custom.min.js' % ui_version)
        a.append('jquery/ui/js/jquery.ui.datepicker.zh.js')
        
    return {'toplinks':a}
