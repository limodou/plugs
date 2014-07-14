def call(version2=False):
    a = []
    a.append('jqutils/jqrmselect.css')
    if version2:
        a.append('jqutils/jqrmselect2.js')
    else:
        a.append('jqutils/jqrmselect.js')
    return {'toplinks':a, 'depends':[('jquery', {'ui':True}), 'jqutils']}
