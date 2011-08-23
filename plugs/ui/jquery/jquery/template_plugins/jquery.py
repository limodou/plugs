def call(app, var, env, version='1.5.2', ui=False, theme='redmond', css_only=False, ui_version='1.8.13', ajax_error=False):
    a = []
    if css_only:
        return {'toplinks':['jquery/ui/css/%s/jquery-ui-%s.custom.css' % (theme, ui_version)]}
    if version:
        a.append('jquery/jquery-%s.min.js' % version)
    if ui:
        a.append('jquery/ui/css/%s/jquery-ui-%s.custom.css' % (theme, ui_version))
        a.append('jquery/jquery-%s.min.js' % version)
        a.append('jquery/ui/js/jquery-ui-%s.custom.min.js' % ui_version)
        a.append('jquery/ui/js/jquery.ui.datepicker.zh.js')
        
    if ajax_error:
        a.append("""<script>$(function(){
    $(document).ajaxError(function(e, xhr, settings, exception) { 
        alert('error in: ' + settings.url + ' \\n'+'error:\\n' + 'ajax request process error!' ); 
    });
}); </script>""")
        
    return {'toplinks':a}
