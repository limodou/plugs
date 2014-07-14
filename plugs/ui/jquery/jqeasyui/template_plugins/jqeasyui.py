def call(theme='simple'):
    a = []
    a.append('jqeasyui/themes/%s/easyui.css' % theme)
    a.append('jqeasyui/themes/icon.css')
    a.append('jqeasyui/jquery.easyui.min.js')
    a.append('jqeasyui/locale/easyui-lang-zh_CN.js')
    return {'toplinks':a}
