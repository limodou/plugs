def call():
    a = []
    a.append('uligantt/d3.min.js')
    a.append('uligantt/jquery.cookie.js')
    a.append('uligantt/mmGrid.css')
    a.append('uligantt/mmGrid.js')
    a.append('uligantt/uliTreeGrid.css')
    a.append('uligantt/uliTreeGrid.js')
    a.append('uligantt/uliGantt.css')
    a.append('uligantt/uliGantt.js')
    a.append('uligantt/splitter.css')
    a.append('uligantt/splitter.js')
    a.append('uligantt/jquery.jeditable.js')
    a.append('uligantt/jquery.jeditable.datepicker.js')
    a.append('<!--[if lt IE 9]>')
    a.append('<script src="/static/uligantt/style-shim.js"></script>')
    a.append('<![endif]-->')

    
    return {'toplinks':a, 'depends':['jquery', 'json2']}
