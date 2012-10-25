def call(app, var, env, ajaxForm=False):
    a = []
    a.append('jqutils/jquery.json-2.3.min.js')
    return {'toplinks':a, 'depends':['jquery']}
