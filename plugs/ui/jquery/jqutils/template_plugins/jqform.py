def call(app, var, env, ajaxForm=False):
    a = []
    a.append('jqutils/jquery.form.js')
    return {'toplinks':a, 'depends':['jquery']}
