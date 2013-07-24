#coding=utf-8
from uliweb.form import *
from uliweb.i18n import ugettext_lazy as _
import uliweb

class FileUploadForm(Form):
    filedata = FileField('上传文件', required=True)
    title = StringField('显示文件名')
    
    def validate_filedata(self, data):
        data['file'].seek(0, 2)
        size = data['file'].tell()
        data['file'].seek(0)
        if size > uliweb.settings.PARA.FORUM_UPLOAD_FILE_SIZE:
            return '文件不能超过 %dK' % (uliweb.settings.PARA.FORUM_UPLOAD_FILE_SIZE/1024)
    
class ImageUploadForm(Form):
    filedata = FileField('上传文件', required=True)
    is_thumbnail = BooleanField('是否进行缩略处理')

    def validate_filedata(self, data):
        from PIL import Image

        data['file'].seek(0, 2)
        size = data['file'].tell()
        data['file'].seek(0)
        if size > uliweb.settings.PARA.FORUM_UPLOAD_IMAGE_SIZE:
            return '文件不能超过 %dK' % (uliweb.settings.PARA.FORUM_UPLOAD_IMAGE_SIZE/1024)
        
        try:
            Image.open(data['file'])
            data['file'].seek(0)
        except Exception, e:
            return '上传文件不是图形文件'
    