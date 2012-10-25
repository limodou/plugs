def call(app, var, env):
    a = []
    a.append('treetable/jquery.treeTable.css')
    a.append('treetable/jquery.treeTable.js')
    return {'toplinks':a, 'depends':[('jquery')]}
