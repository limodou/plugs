def call(app, var, env, ajaxForm=False):
    a = []
    a.append('jqutils/ui.totop.css')
    a.append('jqutils/jquery.ui.totop.js')
    return {'toplinks':a, 'depends':['jquery']}
