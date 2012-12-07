def call(app, var, env, ajaxForm=False, hoverIntent=False, spin=False):
    a = []
    a.append('treetable/treecollapse.css')
    a.append('treetable/treecollapse.js')
    return {'toplinks':a, 'depends':[('jquery')]}
