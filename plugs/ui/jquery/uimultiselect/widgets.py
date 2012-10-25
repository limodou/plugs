from uliweb.form import SelectField

class UIMultiSelectField(SelectField):
    def __init__(self, label='', default=None, choices=None, required=False, 
        validators=None, name='', html_attrs=None, help_string='', build=None, 
        empty='', size=10, selected_list=2, **kwargs):
        super(UIMultiSelectField, self).__init__(label=label, default=default, 
        choices=choices, required=required, validators=validators, name=name, 
        html_attrs=html_attrs, help_string=help_string, build=build, empty=empty, multiple=True, **kwargs)
        self.selected_list = selected_list
        
    def html(self, data, py=True):
        return self.pre_html() + super(UIMultiSelectField, self).html(data, py) + self.post_html()
    
    def pre_html(self):
        return '''{{use "jquery", css_only=True}}
{{use "uimultiselect"}}'''
    
    def post_html(self):
        return """<script>
$(function() {
        $('#%s').multiselect({selectedList:%d});
    });
</script>""" % (self.id, self.selected_list)

        