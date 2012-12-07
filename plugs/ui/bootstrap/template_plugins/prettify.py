def call(app, var, env, theme=None):
    a = ['bootstrap/asset/prettify.css', 'bootstrap/asset/prettify.js']
    if theme and theme!='default':
        a.append('bootstrap/asset/%s.css' % theme)
    return {'toplinks':a}
