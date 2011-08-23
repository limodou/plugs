def call(app, var, env):
    a = []
    a.append('jcrop/jquery.Jcrop.css')
    a.append('jcrop/jquery.Jcrop.min.js')
    return {'toplinks':a, 'depends':['jquery']}
