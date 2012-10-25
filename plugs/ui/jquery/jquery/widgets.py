from uliweb.form.widgets import Text

class DatePicker(Text):
    
#    def pre_html(self):
#        return '{{use "jquery"}}'
#    
    def post_html(self):
        return """<script>
$(function() {
        $('#%(id)s').datepicker({ dateFormat: 'yy-mm-dd' });
    });
</script>"""

        