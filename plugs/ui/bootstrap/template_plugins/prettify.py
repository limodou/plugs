def call(app, var, env, theme=None):
    a = ['bootstrap/asset/prettify.css', 'bootstrap/asset/prettify.js']
    if theme:
        a.append('bootstrap/asset/%s.css' % theme)
    return {'toplinks':a}
