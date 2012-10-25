def call(app, var, env):
    a = []
    a.append('jqimgzoom/css/imgzoom.css')
    a.append('jqimgzoom/scripts/jquery.imgzoom.pack.js')
    return {'toplinks':a, 'depends':[('jquery')]}
