def call(app, var, env, ajaxForm=False, version='1.1.11'):
    a = []
    a.append('xheditor/xheditor-%s-zh-cn.min.js' % version)
    return {'toplinks':a, 'depends':[('jquery')]}
