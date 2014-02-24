#coding=utf8
from uliweb.orm import *

class WikiPage(Model):
    name = Field(str, max_length=200, index=True, unique=True, required=True)
    subject = Field(str, max_length=255) #display name
    content = Field(TEXT)
    creator = Reference('user', nullable=True)
    create_time = Field(datetime.datetime, auto_now_add=True)
    modified_user = Reference('user', nullable=True)
    modified_time = Field(datetime.datetime, auto_now_add=True)
    deleted = Field(bool)
    acl = Field(TEXT)
    hits = Field(int, verbose_name='Hit counts')
    enabled = Field(bool)
    cur_user = Reference('user', nullable=True)
    start_time = Field(datetime.datetime, nullable=True)
    
    def new_revision(self):
        '''Create a new ChangeSet with the old content.'''
        from uliweb import request
        from plugs.generic_attachments import get_attachments
        from uliweb.utils.common import safe_str
        
        #if page is not eanbled then return directly
        if not self.enabled: return 
    
        def get_files():
            result = []
            for x in get_attachments(self):
                result.append('%-70s  %-12s  %s' % (safe_str(x.filename), safe_str(unicode(x.submitter)), str(x.created_date)))
                
            return '\n'.join(result)
    
        latest_version = self.changeset.order_by(WikiChangeSet.c.id.desc()).one()
        files = get_files()
        if (not latest_version or 
                self.content != latest_version.old_content or 
                self.subject != latest_version.old_subject or
                files != latest_version.old_attachments):
                  
            editor = request.user.id if request.user else None
            cs = WikiChangeSet(
                wiki=self,
                editor=editor,
                old_content=self.content,
                old_subject=self.subject,
                old_attachments=files)
            cs.save()
        else:
            cs = latest_version
        return cs
    
    def get_content(self):
        if self.acl:
            return self.acl + '\n' + self.content
        else:
            return self.content
    
    def get_parent(self):
        if '/' in self.name:
            parent = self.get(self.c.name == self.name.rsplit('/', 1)[0])
            return parent
        
    def __unicode__(self):
        return self.subject or self.name
    
    @property
    def es_doc(self):
        # retrun es doc
        doc = {}
        doc['id'] = self.id
        doc['title'] = self.name
        doc['url'] = '/wiki/' + self.name
    
        try:
            doc['author'] = unicode(self.modified_user.nickname)
        except:
            doc['author'] = ''
        doc['content'] = self.content
        doc['created_date'] = self.create_time
        doc['modified_date'] = self.modified_time
        doc['type'] = 'wikipage'
        return doc
        
class WikiChangeSet(Model):
    wiki = Reference('wikipage', collection_name='changeset')
    editor = Reference('user', nullable=True)
    revision = Field(int)
    old_content = Field(TEXT)
    old_subject = Field(str, max_length=255)
    old_attachments = Field(PICKLE)
    modified_time = Field(datetime.datetime, auto_now_add=True)
    reverted = Field(bool)
    
    def save(self):
        if self.id is None:
            lastest = WikiChangeSet.filter(WikiChangeSet.c.wiki==self.wiki.id)\
                .order_by(WikiChangeSet.c.id.desc()).one()
#            lastest = list(WikiChangeSet.filter(WikiChangeSet.c.wiki==self.wiki.id)\
#                .order_by(WikiChangeSet.c.id.desc()))[0]
            if lastest:
                self.revision = lastest.revision + 1
            else:
                self.revision = 1
        super(WikiChangeSet, self).save()
    
