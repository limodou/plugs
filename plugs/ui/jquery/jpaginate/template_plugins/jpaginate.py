def call(app, var, env, ajaxForm=False):
    a = []
    a.append('jpaginate/style.css')
    a.append('jpaginate/jquery.paginate.js')
    return {'toplinks':a, 'depends':[('jquery')]}
