def call(app, var, env, adapter='jquery', html5only=False):
    a = []
    a.append('history/history.adapter.%s.js' % adapter)
    a.append('history/history.js')
    if not html5only:
        a.append('history/history.html4.js')
    return {'toplinks':a, 'depends':['jquery', 'json2']}
