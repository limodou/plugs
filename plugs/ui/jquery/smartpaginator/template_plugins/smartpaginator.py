def call(app, var, env):
    a = []
    a.append('smartpagination/smartpaginator.css')
    a.append('smartpagination/smartpaginator.js')
    return {'toplinks':a}
