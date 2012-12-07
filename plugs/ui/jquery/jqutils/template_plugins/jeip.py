def call(app, var, env, ajaxForm=False):
    a = []
    a.append('jqutils/jeip.js')
    return {'toplinks':a, 'depends':['jquery']}
