#coding=utf-8
import os
from uliweb import expose, functions
from . import AttachmentsFileServing
from werkzeug.exceptions import Forbidden

def uploadfile():
    from uliweb.form import Form, FileField
    from uliweb.utils.image import test_image, thumbnail_image
    
    fileserving = AttachmentsFileServing()
    
    Attachment = functions.get_model('generic_attachment')
    
    class UploadForm(Form):
        fileupload = FileField()
        
        def form_validate(self, data):
            error = {}
            return error
    
    form = UploadForm()
    table = request.GET.get('table')
    id = request.GET.get('id')
    slug = request.GET.get('slug')
    if form.validate(request.values, request.files):
        dir = settings.Generic_Attachment_Save_Dirs.get(table)
        if not dir:
            raise Exception("Saving directory of table %s is not defined in Generic_Attachment_Save_Dirs" % table)
        
        if id:
            path = os.path.join(dir, id)
        else:
            path = dir
        filename = fileserving.save_file(os.path.join(path, form.fileupload.data.filename), form.fileupload.data.file)
        is_image = test_image(filename)
        if is_image and settings.get_var('Generic_Attachment_FileServing/THUMBNAIL_PROCESS'):
            thumbnail_path, thumbnail = thumbnail_image(functions.get_filename(filename, filesystem=True), filename, settings.get_var('Generic_Attachment_FileServing/IMAGE_THUMBNAIL_SIZE'))
            thumbnail_url = functions.get_href(thumbnail)
        else:
            thumbnail = ''
            thumbnail_url = ''
        f = Attachment(filepath=filename, filename=form.fileupload.data.filename, 
            submitter=request.user.id, is_image=is_image, thumbnail_path=thumbnail)
        if slug:
            f.slug = slug
        else:
            f.content_object = (table, id)
        f.save()
        url = fileserving.get_url(filename, title=f.filename, query_para={'alt':f.filename}, _class='filedown')
        href = fileserving.get_href(filename, alt=f.filename)
        return json({'success':True, 'filename':f.filename, 
            'url':url, 'href':href, 'id':f.id, 'submitter':unicode(request.user),
            'is_image':is_image, 'thumbnail_url':thumbnail_url,
            'created_date':str(f.created_date)}, content_type="text/html;charset=utf-8")
    else:
        #如果校验失败，则再次返回Form，将带有错误信息
        return json({'success':False}, content_type="text/html;charset=utf-8")

def deletefile(f_id):
    from uliweb.utils.common import log
    
    fileserving = AttachmentsFileServing()
    
    Attachment = functions.get_model('generic_attachment')
    Tables = functions.get_model('tables')
    
    obj = Attachment.get(int(f_id))
    if obj:
        
        #get tablename
        tablename = Tables.get(obj.table_id)
        check_func = settings.Generic_Attachment_Download_Checking.get(tablename)
        if check_func:
            enable = check_func(obj.content_object, request.user, 'delete')
        else:
            enable = True
        
        if enable:
            filename = obj.filepath
            obj.delete()
            try:
                fileserving.delete_filename(filename)
            except Exception as e:
                log.exception(e)
        else:
            raise Forbidden("You have no permission to delete the file.")
        
    return json({'success':True})

def downloadfile(f_id):
    from uliweb import request
    import urllib2
    
    fileserving = AttachmentsFileServing()
    
    Attachment = functions.get_model('generic_attachment')
    Tables = functions.get_models('tables')

    obj = Attachment.get(int(f_id))
    if not obj:
        error(_("Can't find the file record of {0}").format(f_id))
        
    #get tablename
    tablename = Tables.get_tablename(obj.table_id)
    check_func = settings.Generic_Attachment_Download_Checking.get(tablename)
    if check_func:
        enable = check_func(obj.content_object, request.user, 'download')
    else:
        enable = True
    if enable:
        alt_filename = urllib2.unquote(obj.filename)
        _filename = fileserving.get_filename(filename, False, convert=False)
        x_filename = filename
        return fileserving.download(alt_filename, real_filename=_filename, x_filename=x_filename)
    else:
        raise Forbidden("You have no permission to download the file.")
    
def postimage():
    """
    处理HTML5文件上传
    """
    import base64
    from StringIO import StringIO
    from uliweb.utils.image import thumbnail_image, fix_filename
    from uliweb.form import Form, FileField
    
    fileserving = AttachmentsFileServing()
    
    Attachment = functions.get_model('generic_attachment')
    table = request.values.get('table')
    id = request.values.get('id')
    slug = request.values.get('slug')
    if request.method == 'POST':
        
        dir = settings.Generic_Attachment_Save_Dirs.get(table)
        if not dir:
            raise Exception("Saving directory of table %s is not defined in Generic_Attachment_Save_Dirs" % table)
        
        if id:
            path = os.path.join(dir, id, request.values.get('filename'))
        else:
            path = os.path.join(dir, request.values.get('filename'))
            
        fobj = StringIO(base64.b64decode(request.params.get('data')))
        filename = functions.save_file(path, fobj)
        if settings.get_var('Generic_Attachment_FileServing/THUMBNAIL_PROCESS'):
            thumbnail_path, thumbnail = thumbnail_image(functions.get_filename(filename, filesystem=True), filename, settings.get_var('Generic_Attachment_FileServing/IMAGE_THUMBNAIL_SIZE'))
            thumbnail_url = functions.get_href(thumbnail)
        else:
            thumbnail = ''
            thumbnail_url = ''
        fname = os.path.splitext(os.path.basename(filename))[0].split(',')[-1][:8]
        f = Attachment(filepath=filename, filename=fname, is_image=True,
            submitter=request.user.id, thumbnail_path=thumbnail)
        if slug:
            f.slug = slug
        else:
            f.content_object = (table, id)
        f.save()
        url = fileserving.get_url(filename, title=f.filename, alt=f.filename, _class='filedown')
        href = fileserving.get_href(filename, title=f.filename, query_para={'alt':f.filename})
        return json({'success':True, 'filename':f.filename, 'submitter':unicode(request.user),
            'url':url, 'href':href, 'is_image':f.is_image,
            'id':f.id, 'created_date':str(f.created_date), 'thumbnail_url':thumbnail_url,
            })
  