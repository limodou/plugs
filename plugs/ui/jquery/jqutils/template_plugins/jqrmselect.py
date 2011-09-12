def call(app, var, env, ajaxForm=False):
    a = []
    a.append('jqutils/jqrmselect.css')
    a.append('jqutils/jqrmselect.js')
    return {'toplinks':a, 'depends':[('jquery', {'ui':True}), 'jqutils']}
