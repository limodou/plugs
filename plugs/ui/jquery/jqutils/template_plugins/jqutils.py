def call(app, var, env, ajaxForm=False, hoverIntent=False, spin=False):
    a = []
    depends = [('jquery', {'ui':True})]
    a.append('jqutils/jqutils.css')
    if spin:
        a.append('jqutils/spin.min.js')
    a.append('jqutils/jqrselect.js')
    a.append('jqutils/jqutils.js')
    if ajaxForm:
        depends.append('jqform')
    if hoverIntent:
        a.append('jqutils/jquery.hoverIntent.minified.js')
    return {'toplinks':a, 'depends':depends}
