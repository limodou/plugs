from uliweb.form import *

class WikiEdit(Form):
    content = TextField(label='Content', rows=15, required=True, datatype=unicode)
    name = HiddenField()
    slug = HiddenField()