def call(app, var, env, ajaxForm=False):
    a = []
    a.append('xheditor/xheditor-1.1.9-zh-cn.min.js')
    return {'toplinks':a, 'depends':[('jquery')]}
