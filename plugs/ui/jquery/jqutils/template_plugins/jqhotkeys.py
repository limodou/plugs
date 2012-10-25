def call(app, var, env, ajaxForm=False):
    a = []
    a.append('jqutils/jquery.hotkeys.js')
    return {'toplinks':a, 'depends':['jquery']}
