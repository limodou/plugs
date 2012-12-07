def call(app, var, env, ajaxForm=False):
    a = []
    a.append('jqutils/jquery.cookie.js')
    return {'toplinks':a, 'depends':['jquery']}
