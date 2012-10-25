def call(app, var, env, locale=None):
    a = []
    depends = [('jquery', {'ui':True})]
    a.append('jqtimepicker/jquery-ui-timepicker-addon.css')
    a.append('jqtimepicker/jquery-ui-timepicker-addon.js')
    a.append('jqtimepicker/jquery-ui-sliderAccess.js')
    if locale:
        a.append('jqtimepicker/localization/jquery-ui-timepicker-%s.js' % locale)
    return {'toplinks':a, 'depends':depends}
