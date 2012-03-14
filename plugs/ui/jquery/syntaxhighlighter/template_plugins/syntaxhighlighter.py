def call(app, var, env, theme='Default'):
    a = []
    a.append('syntaxhighlighter/styles/shCore.css')
    a.append('syntaxhighlighter/styles/shTheme%s.css' % theme)
    a.append('syntaxhighlighter/scripts/XRegExp.js')
    a.append('syntaxhighlighter/scripts/shCore.js')
    a.append('syntaxhighlighter/scripts/shAutoloader.js')
    return {'toplinks':a}
