def call(app, var, env, theme="bootstrap"):
    a = []
    depends = [('jquery', {'ui':True})]
    a.append('tablefixedheader/jquery.fixheadertable.css')
    if theme == 'bootstrap':
        a.append('tablefixedheader/theme_bootstrap.css')
    a.append('tablefixedheader/jquery.fixheadertable.js')
    return {'toplinks':a, 'depends':depends}
