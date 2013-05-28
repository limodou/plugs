#coding=utf-8
from uliweb import expose, functions, settings
from werkzeug import cached_property
from uliweb.i18n import ugettext_lazy as _

def parse_acl(line):
    acl = []
    for t in line.split():
        n, p_ = t.split(':')
        permissions = set([x.strip() for x in p_.split(',')])
        
        if not n or not permissions:
            continue
        
        d = {}
        if n[0] == '+':
            d['mode'] = '+'
            n = n[1:]
        elif n[0] == '-':
            d['mode'] = '-'
            n = n[1:]
        else:
            d['mode'] = ''
        
        if not n:
            continue
        if n[0] == '[':
            pos = n.find(']')
            if pos > -1:
                _type = n[1:pos].strip().lower()
                n = n[pos+1:]
            else:
                continue
        else:
            _type = 'user'
        d['perms'] = set(permissions)
        d['name'] = n
        d['type'] = _type
        
        acl.append(d)
    return acl
    
def find_acl(text):
    """
    Access Control see also http://moinmo.in/HelpOnAccessControlLists
    
    #acl [+-]username|[group]groupname|[role]rolename:read,write,delete,revert,admin
    
    #acl can be multiple lines, and it should be the first lines of contents
    
    When a user is trying to access an ACL-protected resource, the ACL entries 
    will be processed in the order they are found. The first ACL entry matching 
    the user will determine whether the user has access to that resource or not 
    and processing will stop. Due to this first match algorithm, you should 
    arrange your ACL entries in the following order: 1) single usernames, 2) 
    special groups, 3) more general groups, 4) All.
    
    """
    import re
    
    #acl = {'name':xxx, 'type':'group|role|user', 'mode':'enable|disable|replace'}
    acl = []
    acl_lines = []
    i = 0
    if text:
        for i, line in enumerate(text.splitlines()):
            if line and line.startswith('#acl '):
                acl_lines.append(line)
                r = parse_acl(line[5:])
                acl.extend(r)
            else:
                break
            
    return acl, '\n'.join(acl_lines), i

@expose('/wiki')
class WikiView(object):
    def __init__(self):
        self.model = functions.get_model('wikipage')
        self.changeset = functions.get_model('wikichangeset')
        
    def _get_page_html(self, text):
        from par.bootstrap_ext import blocks
#        from md_ext import new_code_comment
        from par.md import MarkdownGrammar as grammar
        from par.md import MarkdownHtmlVisitor as parser
        
        if not text:
            return ''
        i = 0
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line:
                if line.startswith('#acl '):
                    continue
                elif not line.strip():
                    continue
                else:
                    break
            else:
                break
            
        g = grammar()
        result, rest = g.parse('\n'.join(lines[i:]), resultSoFar=[], skipWS=False)
        
#        blocks['code-comment'] = new_code_comment
        cls = 'prettyprint linenums'
        t = parser(grammar=g, tag_class={'table':'table table-bordered', 
                'pre':cls}, 
            block_callback=blocks)
            
        content = t.visit(result, root=True)
        return content
    
    @cached_property
    def _get_default_acl(self):
        from uliweb import settings
        
        return parse_acl(settings.WIKI.WIKI_ACL_DEFAULT)
    
    def _check_permission(self, perm, acl=None, user=None, 
        err_msg=_("You have no right to access the page."), raise_exception=True):
        from uliweb.orm import Model
        
        if isinstance(acl, Model):
            acl = acl.acl
        else:
            acl = acl
        result = self._find_permissions(perm, acl, user)
        if not result.get(perm, False):
            if raise_exception:
                error(err_msg)
            else:
                return False
        return True
            
    def _find_permissions(self, perms, acl=None, user=None):
        """
        Check permission of one page, or just get default acl
        
        perms can be single value or a list value
        """
        from uliweb import request
        
        _acl = self._get_default_acl
        if isinstance(acl, (str, unicode)):
            page_acl, acl_lines, i = find_acl(acl)
        elif isinstance(acl, dict):
            page_acl = acl
        else:
            page_acl = []
        
        if not user:
            user = request.user
            
        if not isinstance(perms, (tuple, list)):
            p = set([perms])
        else:
            p = set(perms)
            
        #perms result
        result = {}
        for d in page_acl + _acl:
            find = False
            if not p:
                break
            if d['type'] == 'user':
                if d['name'] == 'All':
                    find = True
                else:
                    if user and user.username == d['name']:
                        find = True
            elif d['type'] == 'role':
                if functions.has_role(user, d['name']):
                    find = True
                    
            #todo check other type according settings.ini
            if find:
                f_perms = p.intersection(d['perms'])
                if f_perms:
                    p.difference_update(f_perms)
                    for x in f_perms:
                        #if mode is not '-', then think it's enable
                        #otherwise disable
                        result[x] = d['mode'] != '-'
                if d['mode'] in ('+', '-'):
                    continue
                else:
                    break

        return result
    
    @expose('', defaults={'pagename':''})
    @expose('<pagename>')
    def wiki_page(self, pagename):
        if not pagename:
            if 'pages' in request.GET:
                response.template = 'WikiView/wiki_pages.html'
                objects = self.model.filter(self.model.c.deleted==False).fields('name').order_by(self.model.c.name)
                
                return {'objects':objects}
            
            return redirect(url_for(self.__class__.wiki_page, pagename='Index'))
        
        wiki = self.model.get(self.model.c.name == pagename)
        
        if not wiki:
            #check read permission
            self._check_permission('read')
            
            if pagename == 'Index':
                content = settings.WIKI.IndexContent
                wiki = self.model(name='Index', content=content)
                wiki.save()
                wiki.new_revision(wiki.content)
        
        if wiki:
            #check read permission
            self._check_permission('read', wiki)
            
            rev = int(request.GET.get('rev', 0))
            rev_time = None
            if rev:
                r = self.changeset.get((self.changeset.c.wiki==wiki.id) & (self.changeset.c.revision==rev))
                rev_time = r.modified_time and r.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                content = self._get_page_html(r.old_content)
            else:
                content = self._get_page_html(wiki.content)
            return {'object':wiki, 'content':content, 'revision':rev, 
                'rev_time':rev_time, 
                'permissions':self._find_permissions(['read', 'write', 'delete', 'revert', 'admin'], wiki.acl)}
        else:
            #check read permission
            self._check_permission('write')
            
            return redirect(url_for(self.__class__.wiki_edit, pagename=pagename))

    @expose('<pagename>/preview')
    def wiki_preview(self, pagename):
        content = self._get_page_html(request.POST.get('content') or 'No conent')
        return json({'success':True, 'data':content})
    
    @expose('<pagename>/edit')
    def wiki_edit(self, pagename):
        from forms import WikiEdit
        from uliweb.utils.common import get_uuid
        from plugs.generic_attachments import enable_attachments
        
        wiki = self.model.get(self.model.c.name == pagename)
        #check read permission
        self._check_permission('write', wiki)
        
        if wiki:
            data = wiki.to_dict()
            slug = wiki
        else:
            data = {}
            slug = get_uuid()
            data['slug'] = slug
        
        form = WikiEdit(data=data)
        if request.method == 'GET':
            return {'pagename':pagename, 'form':form, 'slug':slug}
        elif request.method == 'POST':
            if form.validate(request.POST):
                if wiki:
                    #check admin permission
                    old_acl, old_acl_lines, old_begin = find_acl(wiki.acl)
                    acl, acl_lines, begin = find_acl(form.content.data)
                    if old_acl_lines != acl_lines:
                        if not self._check_permission('admin', old_acl, raise_exception=False):
                            flash(_('You have no right to change the acl info.'))
                        else:
                            wiki.acl = acl_lines
                    lines = form.content.data.rstrip().splitlines()
                    if wiki.acl:
                        wiki.content = '\n'.join([wiki.acl] + lines[begin:])
                    else:
                        wiki.content = '\n'.join(lines[begin:])
                    wiki.modified_user = request.user.id
                    wiki.save()
                    wiki.new_revision(wiki.content)
                    
                    #enable attachments
                    enable_attachments(wiki, 'wiki')
                else:
                    #check admin permission
                    wiki = self.model(name=pagename,  
                        content=form.content.data.strip(), creator=request.user.id, 
                        modified_user=request.user.id)
                    acl, acl_lines, begin = find_acl(form.content.data)
                    if acl_lines:
                        if not self._check_permission('admin', raise_exception=False):
                            flash(_('You have no right to change the acl info.'))
                            wiki.acl = ''
                        else:
                            wiki.acl = acl_lines
                    else:
                        wiki.acl = ''
                    lines = form.content.data.rstrip().splitlines()
                    if wiki.acl:
                        wiki.content = '\n'.join([wiki.acl] + lines[begin:])
                    else:
                        wiki.content = '\n'.join(lines[begin:])
                    wiki.save()
                    wiki.new_revision(wiki.content)
                    
                    #enable attachments
                    enable_attachments(form.slug.data, 'wiki')
                    
                return redirect(url_for(self.__class__.wiki_page, pagename=pagename))
            else:
                return {'pagename':pagename, 'form':form, 'slug':form.slug.data}
            
    @expose('<pagename>/delete')
    def wiki_delete(self, pagename):
        wiki = self.model.get(self.model.c.name == pagename)
        if wiki:
            #check read permission
            self._check_permission('delete', wiki)
            
            self.changeset.filter(self.changeset.c.wiki == wiki.id).remove()
            wiki.delete()
            return redirect(url_for(self.__class__.wiki_page))
        else:
            error("The page %s is not existed, please check!" % pagename)
        
    @expose('<pagename>/revision')
    def wiki_revision(self, pagename):
        wiki = self.model.get(self.model.c.name == pagename)
        if wiki:
            changeset = wiki.changeset.all().order_by(self.changeset.c.revision.desc())
            return {'wiki':wiki, 'changeset':changeset, 'can_revert':self._check_permission('revert', wiki.acl, raise_exception=False)}
        else:
            error("The page %s is not existed, please check!" % pagename)
        
    @expose('<pagename>/diff')
    def wiki_diff(self, pagename):
        from diff2html import diff2html

        rev1 = int(request.GET['rev1'])
        rev2 = int(request.GET['rev2'])
        
        wiki = self.model.get(self.model.c.name == pagename)
        
        #check read permission
        self._check_permission('read', wiki)

        c1 = self.changeset.get((self.changeset.c.wiki == wiki.id) & (self.changeset.c.revision==rev1))
        c2 = self.changeset.get((self.changeset.c.wiki == wiki.id) & (self.changeset.c.revision==rev2))
        
        content = self._diff(c1.old_content, c2.old_content)
        fileinfo = '%s <a href="%s">r%d</a> - <a href="%s">r%d</a>' % (pagename,
            url_for(self.__class__.wiki_page, pagename=pagename, rev=rev2),
            rev2,
            url_for(self.__class__.wiki_page, pagename=pagename, rev=rev1),
            rev1,
            )
        diff_content = diff2html(pagename, pagename, content, fileinfo=fileinfo)
        return {'pagename':pagename, 'content':diff_content}

    def _diff(self, txt1, txt2):
        from difflib import unified_diff
        
        return unified_diff(txt1.splitlines(), txt2.splitlines())

    @expose('<pagename>/revert')
    def wiki_revert(self, pagename):
        wiki = self.model.get(self.model.c.name == pagename)
        
        #check read permission
        self._check_permission('revert', wiki)
        
        rev = int(request.GET['rev'])
        r = self.changeset.get((self.changeset.c.wiki==wiki.id) & (self.changeset.c.revision==rev))
        if (wiki.content != r.old_content) :
            wiki.content = r.old_content
            wiki.save()
            wiki.new_revision(wiki.content)
        return redirect(url_for(self.__class__.wiki_page, pagename=pagename))
        
