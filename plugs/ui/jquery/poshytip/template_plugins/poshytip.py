def call(app, var, env, theme=['twitter', 'yellow', 'yellowsimple']):
    a = []
    for t in theme:
        a.append('poshytip/tip-%s/tip-%s.css' % (t, t))
    if 'yellowsimple' not in theme:
        t = 'yellowsimple'
        a.append('poshytip/tip-%s/tip-%s.css' % (t, t))
#    a.append('poshytip/jquery.poshytip.min.js')
    a.append('poshytip/jquery.poshytip.js')
    return {'toplinks':a, 'depends':[('jquery')]}
