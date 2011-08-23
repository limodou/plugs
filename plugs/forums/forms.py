#coding=utf-8
from uliweb.form import *
from uliweb.i18n import ugettext_lazy as _

class FileUploadForm(Form):
    filedata = FileField('上传文件', required=True)
    title = StringField('显示文件名')
    
class ImageUploadForm(Form):
    filedata = FileField('上传文件', required=True)
    is_thumbnail = BooleanField('是否进行缩略处理')
