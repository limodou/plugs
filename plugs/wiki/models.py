#coding=utf8
from uliweb.orm import *

class WikiPage(Model):
    name = Field(str, max_length=200, index=True, unique=True)
    content = Field(TEXT)
    creator = Reference('user')
    create_time = Field(datetime.datetime, auto_now_add=True)
    modified_user = Reference('user')
    modified_time = Field(datetime.datetime, auto_now_add=True, auto_now=True)
    deleted = Field(bool)
    acl = Field(TEXT)
    hits = Field(int, verbose_name='Hit counts')
    
    def new_revision(self, old_content='', editor=None):
        '''Create a new ChangeSet with the old content.'''
        from uliweb import request
        
        cs = WikiChangeSet(
            wiki=self,
            editor=editor or request.user.id,
            old_content=old_content)
        cs.save()
        
        return cs
    
    def get_content(self):
        if self.acl:
            return self.acl + '\n' + self.content
        else:
            return self.content
        
class WikiChangeSet(Model):
    wiki = Reference(WikiPage, collection_name='changeset')
    editor = Reference('user')
    revision = Field(int)
    old_content = Field(TEXT)
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
    
