from uliweb.form import SelectField

class JQComboBoxField(SelectField):
    def __init__(self, label='', default=None, choices=None, required=False, 
        validators=None, name='', html_attrs=None, help_string='', build=None, 
        empty='', size=10, url=None, get_record=None, **kwargs):
        super(JQComboBoxField, self).__init__(label=label, default=default, 
        choices=None, required=required, validators=validators, name=name, 
        html_attrs=html_attrs, help_string=help_string, build=build, empty=empty, **kwargs)
        self.url = url
        self._default = self._default or ''
        self.choices = [(self._default, self.empty)]
        self.get_record = get_record
        
    def html(self, data, py=True):
        if self.get_record:
            self.choices = self.get_record(data)
        return self.pre_html() + super(JQComboBoxField, self).html(data, py) + self.post_html()
    
    def pre_html(self):
        return '''{{use "jquery"}}
{{use "jqcombobox"}}'''
    
    def post_html(self):
        return """<script>
$(function() {
        $('#%s').sexyCombo({'initialHiddenValue':%r, 'emptyText':'%s', 
            'lazyGetDataUrl':'%s'});
    });
</script>""" % (self.id, self.default, self.empty, self.url)

        