def call(app, var, env, include=['drag', 'drop'], version='2.0'):
    a = []
    for x in include:
        a.append('jqutils/jquery.event.%s-%s.min.js' % (x, version))
    return {'toplinks':a, 'depends':['jquery']}