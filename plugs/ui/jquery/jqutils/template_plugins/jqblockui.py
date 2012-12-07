def call(app, var, env, ajaxForm=False):
    a = []
    a.append('jqutils/jquery.blockUI.js')
    return {'toplinks':a, 'depends':['jquery']}
