def call(app, var, env, version='1.5.2', ui=False, theme='redmond', css_only=False, ui_version='1.8.13', ajax_error=False):
    a = []
    a.append('ztree/style/zTreeStyle.css')
    a.append('ztree/style/zTreeIcons.css')
    a.append('ztree/jquery.ztree-2.6.min.js')
        
    return {'toplinks':a, 'depends':['jquery']}
