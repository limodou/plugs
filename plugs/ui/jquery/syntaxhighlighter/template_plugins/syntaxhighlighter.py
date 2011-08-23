def call(app, var, env, ajaxForm=False):
    a = []
    a.append('syntaxhighlighter/styles/shCore.css')
    a.append('syntaxhighlighter/styles/shThemeDefault.css')
    a.append('syntaxhighlighter/scripts/shCore.js')
    a.append('syntaxhighlighter/scripts/shAutoloader.js')
    return {'toplinks':a}
