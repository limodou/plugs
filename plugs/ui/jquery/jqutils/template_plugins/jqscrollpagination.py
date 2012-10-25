def call(app, var, env, ajaxForm=False):
    a = []
    a.append('jqutils/jquery.scrollpagination.js')
    return {'toplinks':a, 'depends':['jquery', 'jqutils']}
