def call(ajaxForm=False):
    a = []
    a.append('jpaginate/css/style.css')
    a.append('jpaginate/jquery.paginate.js')
    return {'toplinks':a, 'depends':[('jquery')]}
