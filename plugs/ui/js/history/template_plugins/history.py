def call(app, var, env, adapter='jquery', html5only=False):
    a = []
    if html5only:
        _type = 'html5'
    else:
        _type = 'html4+html5'
    a.append('history/%s/%s.history.js' % (_type, adapter))
    return {'toplinks':a, 'depends':['jquery']}
