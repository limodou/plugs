def call(app, var, env):
    a = []
    a.append('jqmultiselect/css/ui.multiselect.css')
    a.append('jqmultiselect/js/plugins/localisation/jquery.localisation.min.js')
    a.append('jqmultiselect/js/plugins/scrollTo/jquery.scrollTo-min.js')
    a.append('jqmultiselect/js/ui.multiselect.js')
    return {'toplinks':a}
