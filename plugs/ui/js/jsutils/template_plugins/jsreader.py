def call(app, var, env, version=None):
    from uliweb import settings
    
    a = []
    a.append('jsreader/filereader.js')
    return {'toplinks':a}
