def call(app, var, env):
    a = ['bootstrap/fontawesome/css/font-awesome.css', 
        '''<!--[if IE 7]>
  <link rel="stylesheet" href="/static/bootstrap/fontawesome/css/font-awesome-ie7.css">
<![endif]-->
''',
        ]
    return {'toplinks':a}
