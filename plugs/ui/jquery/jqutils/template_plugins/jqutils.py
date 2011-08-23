def call(app, var, env, ajaxForm=False):
    a = []
    a.append('jqutils/jqutils.js')
    a.append('jqutils/jqrselect.js')
    if ajaxForm:
        a.append('jqutils/jquery.form.js')
    return {'toplinks':a, 'depends':[('jquery', {'ui':True})]}
