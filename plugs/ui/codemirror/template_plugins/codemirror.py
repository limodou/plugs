def call(app, var, env, modes=None):
    from uliweb import settings
    
    a = []
    a.append('codemirror/lib/codemirror.css')
    a.append('codemirror/lib/codemirror.js')
    for x in modes or []:
        a.append('codemirror/mode/%s/%s.js' % (x, x))
    return {'toplinks':a}