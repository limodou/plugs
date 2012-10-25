def call(app, var, env):
    a = []
    a.append('slickgrid/slick.grid.css')
    a.append('slickgrid/slick.core.js')
    a.append('slickgrid/slick.formatters.js')
    a.append('slickgrid/slick.editors.js')
    a.append('slickgrid/slick.grid.js')
    a.append('slickgrid/slick.dataview.js')
    return {'toplinks':a, 'depends':[('jquery', {'ui':True}), ('jqevent', {'include':['drag']})]}