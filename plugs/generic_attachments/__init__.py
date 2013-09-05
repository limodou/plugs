import os
from uliweb import functions
from uliweb.contrib.upload import FileServing
from uliweb.utils.common import log

class AttachmentsFileServing(FileServing):
    default_config = 'Generic_Attachment_FileServing'
    options = {
        'x_sendfile' : ('X_SENDFILE', None),
        'x_header_name': ('X_HEADER_NAME', ''),
        'x_file_prefix': ('X_FILE_PREFIX', '/files'),
        'to_path': ('TO_PATH', './uploads'),
        'buffer_size': ('BUFFER_SIZE', 4096),
        '_filename_converter': ('FILENAME_CONVERTER', None),
    }

def get_attachments(slug_or_obj):
    Attachments = functions.get_model('generic_attachment')
        
    if isinstance(slug_or_obj, (str, unicode)):
        query = Attachments.filter(Attachments.c.slug==slug_or_obj)
    else:
        query = Attachments.content_object.filter(slug_or_obj)
    return query

def enable_attachments(slug, obj, path, movefile=False):
    """
    Used to process new object files upload
    it'll rename the filename to new path and also add content_object according obj
    and if slug is None, then it'll do nothing
    """
    fileserving = AttachmentsFileServing()
    
    for f in get_attachments(slug or obj):
        f.enabled = True
        f.content_object = obj
        if slug and movefile:
            r_filename = fileserving.get_filename(f.filepath, convert=False)
            dir = os.path.dirname(f.filepath)
            _file = os.path.basename(f.filepath)
            new_filename = os.path.join(dir, str(path), _file)
            f.filepath = new_filename
            r_new_filename = fileserving.get_filename(new_filename, convert=False)
            
            #check if the new directory is existed
            new_dir = os.path.dirname(r_new_filename)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            try:
                os.rename(r_filename, r_new_filename)
            except Exception, e:
                log.exception(e)
                log.info("from %s to %s", r_filename, r_new_filename)
        f.save()
        