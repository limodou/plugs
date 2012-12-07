def call(app, var, env):
    a = ['bootstrap/jquery.dialog2/jquery.dialog2.css', 
        'bootstrap/jquery.dialog2/jquery.controls.js',
        'bootstrap/jquery.dialog2/jquery.dialog2.js',
        'bootstrap/jquery.dialog2/jquery.dialog2.helpers.js',
        ]
    return {'toplinks':a, 'depends':['jquery', 'bootstrap']}
