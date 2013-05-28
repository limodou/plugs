import os
from uliweb import functions
from uliweb.contrib.upload import FileServing
from uliweb.utils.common import log

class AttachmentsFileServing(FileServing):
    options = {
        'x_sendfile' : ('Generic_Attachment_FileServing/X_SENDFILE', None),
        'x_header_name': ('Generic_Attachment_FileServing/X_HEADER_NAME', ''),
        'x_file_prefix': ('Generic_Attachment_FileServing/X_FILE_PREFIX', '/files'),
        'to_path': ('Generic_Attachment_FileServing/TO_PATH', './uploads'),
        'buffer_size': ('Generic_Attachment_FileServing/BUFFER_SIZE', 4096),
        '_filename_converter': ('Generic_Attachment_FileServing/FILENAME_CONVERTER', None),
    }

def get_attachments(slug_or_obj):
    Attachments = functions.get_model('generic_attachment')
        
    if isinstance(slug_or_obj, (str, unicode)):
        query = Attachments.filter(Attachments.c.slug==slug_or_obj)
    else:
        query = Attachments.content_object.filter(slug_or_obj)
    return query

def enable_attachments(slug_or_obj, path):
    fileserving = AttachmentsFileServing()
    
    for f in get_attachments(slug_or_obj):
        f.enabled = True
        if isinstance(slug_or_obj, (str, unicode)):
            r_filename = fileserving.get_filename(f.filepath, convert=False)
            dir = os.path.dirname(f.filepath)
            _file = os.path.basename(f.filepath)
            new_filename = os.path.join(dir, path, _file)
            f.filepath = new_filename
            r_new_filename = fileserving.get_filename(new_filename, convert=False)
            try:
                os.rename(r_filename, r_new_filename)
            except Exception, e:
                log.exception(e)
        f.save()
        