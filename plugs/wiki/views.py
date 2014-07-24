#coding=utf-8
from uliweb import expose, functions, settings
from werkzeug import cached_property
from uliweb.i18n import ugettext_lazy as _
from uliweb.utils import date
from uliweb.utils.common import log

def parse_acl(line, acl_alias=None):
    """
    >>> parse_acl('limodou:read')
    [{'perms': set(['read']), 'type': 'user', 'mode': '', 'name': 'limodou'}]
    >>> parse_acl('user1,user2:read,write')
    [{'perms': set(['read', 'write']), 'type': 'user', 'mode': '', 'name': 'user1'}, {'perms': set(['read', 'write']), 'type': 'user', 'mode': '', 'name': 'user2'}]
    >>> parse_acl('[role]user1,user2:read,write')
    [{'perms': set(['read', 'write']), 'type': 'role', 'mode': '', 'name': 'user1'}, {'perms': set(['read', 'write']), 'type': 'role', 'mode': '', 'name': 'user2'}]
    >>> parse_acl('+limodou:read All:read,write')
    [{'perms': set(['read']), 'type': 'user', 'mode': '+', 'name': 'limodou'}, {'perms': set(['read', 'write']), 'type': 'user', 'mode': '', 'name': 'All'}]
    """
    from copy import deepcopy
    
    acl_alias = acl_alias or {}
    
    acl = []
    for t in line.split():
        n, p_ = t.split(':')
        
        p = []
        #add acl replace according to acl_alias
        for x in p_.split(','):
            if x in acl_alias:
                p.extend(acl_alias[x].split(','))
            else:
                p.append(x)
        
        if not n or not p:
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
        d['perms'] = set(p)
        d['type'] = _type
        
        names = n.split(',')
        for t in names:
            x = deepcopy(d)
            x['name'] = t
            acl.append(x)
    return acl
    
def find_acl(text, acl_alias=None):
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
                r = parse_acl(line[5:], acl_alias)
                acl.extend(r)
            else:
                break
            
    return acl, '\n'.join(acl_lines), i

@expose('/wiki')
class WikiView(object):
    def __init__(self):
        self.model = functions.get_model('wikipage')
        self.changeset = functions.get_model('wikichangeset')
        
    def _get_cached_page_html(self, pagename, text, update=False):
        from uliweb.utils.common import safe_str
        from uliweb import settings
        
        if settings.get_var('WIKI/WIKI_PAGE_CACHED'):
            handler = functions.get_staticize(subdir='wiki')
            key = 'wiki/' + pagename
            
            def creator(text=text):
                content, kwargs = self._get_page_html(text)
                return safe_str(repr(kwargs) + '||||' + content)
            
            x = handler.get(key, creator=creator, update=update)
            try:
                kwargs, content = x.split('||||')
            except:
                self._del_cached_page_html(pagename)
                return self._get_page_html(text)
            
            return content, eval(kwargs)
        else:
            return self._get_page_html(text)
        
    def _del_cached_page_html(self, pagename):
        from uliweb import settings
        
        if settings.get_var('WIKI/WIKI_PAGE_CACHED'):
            handler = functions.get_staticize(subdir='wiki')
            handler.delete('wiki/' + pagename)
        
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
            if line.startswith('#acl ')or not line:
                continue
            else:
                break
            
        #读注释 #rem 在注释中可以对页面做一些配置，现在支持：
        # toc=1
        
        find = False
        kw_lines = []
        for j in range(i, len(lines)):
            line = lines[j]
            if line:
                if line.startswith('#rem ') or not line:
                    kw_lines.append(line[4:])
                    find = True
                    continue
                else:
                    break
            
        kwargs = {}
        if find:
            i = j
            for k, v in [x.split('=', 1) for x in ' '.join(kw_lines).split(',') if '=' in x]:
                kwargs[k.strip()] = v.strip()
                
        g = grammar()
        result, rest = g.parse('\n'.join(lines[i:]), resultSoFar=[], skipWS=False)
        
#        blocks['code-comment'] = new_code_comment
        cls = 'prettyprint linenums'
        t = parser(grammar=g, tag_class={'table':'table table-bordered', 
                'pre':cls}, 
            block_callback=blocks)
            
        content = t.visit(result, root=True)
        return content, kwargs
    
    @cached_property
    def _get_default_acl(self):
        from uliweb import settings
        
        return parse_acl(settings.WIKI.WIKI_ACL_DEFAULT)
    
    def _check_permission(self, perm, acl=None, user=None, page=None,
        err_msg=_("You have no right to access the page."), raise_exception=True):
        from uliweb.orm import Model
        
        if not user:
            user = request.user
        
        #superuser can do everything
        if user and user.is_superuser:
            return True
        
        if not user:
            err_msg = _("You are not logged in. ") + err_msg
            
        if isinstance(acl, Model):
            acl = acl.acl
        else:
            acl = acl
            
        if page:
            pagename = page.name
        else:
            pagename = ''
            
        result, _perms = self._find_permissions(perm, acl, user, check_default=False, pagename=pagename)
        while _perms:
            if page:
                parent = page.get_parent()
                if parent:
                    _result, _perms = self._find_permissions(_perms, parent.acl, user, check_default=False, pagename=page.name)
                    result.update(_result)
                    page = parent
                    if not _perms:
                        break
                else:
                    _result, _perms = self._find_permissions(_perms, None, user)
                    result.update(_result)
                    break
            else:
                _result, _perms = self._find_permissions(_perms, None, user)
                result.update(_result)
                break
        if user:
            log.debug('check permission perm=%s, user=%s, result=%r', perm, user.username, result)
        else:
            log.debug('check permission perm=%s, result=%r', perm, result)
        if not result.get(perm, False):
            if raise_exception:
                error(err_msg)
            else:
                return False
        return True
           
    def _find_tree_permissions(self, perms, page=None, user=None):
        if user and user.is_superuser:
            result = dict([(x, True) for x in perms])
            return result
        
        result, _perms = self._find_permissions(perms, page.acl, user, check_default=False)
        while _perms:
            parent = page.get_parent()
            if parent:
                _result, _perms = self._find_permissions(_perms, parent.acl, user, check_default=False, pagename=page.name)
                result.update(_result)
                page = parent
                if not _perms:
                    break
            else:
                _result, _perms = self._find_permissions(_perms, None, user)
                result.update(_result)
                break
            
        if user:
            username = user.username
        else:
            username = 'NO'
        log.debug("find_tree_permissions: perms=%r, user=%s, result=%r, page=%s", perms, username, result, page.name)
        return result
    
    def _find_permissions(self, perms, acl=None, user=None, check_default=True, pagename=''):
        """
        Check permission of one page, or just get default acl
        
        perms can be single value or a list value
        """
        from uliweb import request, settings
        from uliweb.utils.common import import_attr
        
        if check_default:
            _acl = self._get_default_acl
        else:
            _acl = []
        if isinstance(acl, (str, unicode)):
            page_acl, acl_lines, i = find_acl(acl, settings.WIKI_ACL_ALIAS)
        elif isinstance(acl, dict):
            page_acl = acl
        else:
            page_acl = []
        
        if not user:
            user = request.user
            
        if isinstance(perms, (tuple, list)):
            p = set(perms)
        elif isinstance(perms, set):
            p = perms.copy()
        else:
            p = set([perms])
            
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
            #add other type extention
            else:
                if d['type'] in settings.get_var('WIKI/WIKI_ACL_TYPES', {}):
                    func = import_attr(settings.get_var('WIKI/WIKI_ACL_TYPES')[d['type']])
                    if func(user, d['name']):
                        find = True
                    
            if find:
                f_perms = p.intersection(d['perms'])
                if f_perms:
                    p.difference_update(f_perms)
                    for x in f_perms:
                        #if mode is not '-', then think it's enable
                        #otherwise disable
                        result[x] = d['mode'] != '-'
                if p and d['mode'] in ('+', '-'):
                    continue
                else:
                    #set not found perm to False
                    for x in p:
                        result[x] = False
                    p = set()
                    break
        if user:
            username = user.username
        else:
            username = 'NO'
        log.debug("ACL check: perms=%r, user=%s, result=%r, rest=%r, pagename=%s, acl=%s", perms, username, result, p, pagename, acl)
        return result, p
    
    @expose('', defaults={'pagename':''})
    @expose('<path:pagename>')
    def wiki(self, pagename):
        pagename = pagename.rstrip('/')
        action = request.GET.get('action', 'view')
        func_name = '_wiki_' + action
        func = getattr(self, func_name)
        return func(pagename)
    
    def _wiki_view(self, pagename):
        from uliweb import request, response
        
        response.template = 'WikiView/wiki_view.html'
        
        if not pagename:
            if 'pages' in request.GET:
                response.template = 'WikiView/wiki_pages.html'
                objects = self.model.filter(self.model.c.enabled==True).filter(self.model.c.deleted==False).fields('name').order_by(self.model.c.name)
                
                return {'objects':objects}
            
            return redirect(url_for(self.__class__.wiki, pagename='Index'))
        
        wiki = self.model.get((self.model.c.name == pagename) & (self.model.c.enabled==True))
        
        if not wiki:
            #check read permission
            self._check_permission('read')
            
            if pagename == 'Index':
                content = settings.WIKI.IndexContent
                wiki = self.model(name='Index', content=content, enabled=True, creator=request.user, modified_user=request.user)
                wiki.save()
                wiki.new_revision()
        
        if wiki:
            #check read permission
            self._check_permission('read', wiki, page=wiki)
            
            #处理阅读次数
            key = '__wikivisited__:%s:%d' % (request.remote_addr, wiki.id)
            cache = functions.get_cache()
            v = cache.get(key, None)
            if not v:
                self.model.filter(self.model.c.id==int(wiki.id)).update(hits=self.model.c.hits+1)
                cache.set(key, 1, settings.get_var('WIKI/WIKI_VISITED_TIMEOUT'))
            
            rev = int(request.GET.get('rev', 0))
            rev_time = None
            if rev:
                cached_pagename = wiki.name + '&ver=%d' % rev
                r = self.changeset.get((self.changeset.c.wiki==wiki.id) & (self.changeset.c.revision==rev))
                rev_time = r.modified_time and r.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                content, kwargs = self._get_cached_page_html(cached_pagename, r.old_content)
            else:
                cached_pagename = wiki.name
                content, kwargs = self._get_cached_page_html(cached_pagename, wiki.content)
            last_rev = wiki.changeset.order_by(self.changeset.c.id.desc()).one().revision
            return {'wiki':wiki, 'content':content, 'revision':rev, 
                'rev_time':rev_time, 'last_rev':last_rev,
                'page_args':kwargs,
                'create_new':self._check_permission('write', raise_exception=False),
                'permissions':self._find_tree_permissions(['read', 'write', 'delete'], wiki, request.user)
                }
        else:
            #check read permission
            self._check_permission('write')
            
            return redirect(url_for(self.__class__.wiki, pagename=pagename, action='edit'))

    def _wiki_preview(self, pagename):
        from uliweb import request, json
        
        content, kwargs = self._get_page_html(request.POST.get('content') or 'No conent')
        return json({'success':True, 'data':content, 'page_args':kwargs})
    
    def _wiki_edit_child(self, pagename):
        return self._wiki_edit(pagename, child=bool(pagename))
    
    def _wiki_edit(self, pagename, child=False):
        from uliweb import request, response
        from forms import WikiEdit
        from uliweb.utils.common import get_uuid
        from plugs.generic_attachments import enable_attachments
        
        #检查用户是否登录
        functions.require_login()
        
        response.template = 'WikiView/wiki_edit.html'
        
        #if not pagename, then it'll be ':NewPage', and when submit as it, 
        #the form check will complain it an error
        if not pagename:
            pagename = ':NewPage'
        page = pagename

        if child:
            parent = pagename
            page = pagename + '/:NewPage'
        else:
            if '/' in pagename:
                parent = pagename.rsplit('/', 1)[0]
            else:
                parent = ''

        if parent:
            parent_page = self.model.get(self.model.c.name == parent)
            
            #检查父结点是否存在
            if not parent_page or not parent_page.enabled or parent_page.deleted:
                flash('父页面尚未创建，请先创建', 'error')
                return redirect(url_for(self.__class__.wiki, pagename=parent, action='edit'))
            
        wiki = self.model.get(self.model.c.name == page)
        if wiki and wiki.enabled and not wiki.deleted:
            #check write permission
            self._check_permission('write', wiki, page=wiki)
        else:
            if parent:
                self._check_permission('write', parent_page, page=parent_page)
            else:
                self._check_permission('write')
        
        form = WikiEdit()
        WikiEdit.name.label = u'页面名称'
        if parent:
            WikiEdit.name.label = u'页面名称 %s/' % parent
            
        if request.method == 'GET':
            #if no wiki page existed, then create one first, but will not create revision
            #check if the wiki is not enabled then delete it first
            if wiki and (not wiki.enabled or wiki.deleted):
                self._delete_wikipage(wiki, real=True)
                
                wiki = self.model(name=page, creator=request.user, modified_user=request.user)
            
            if not wiki:
                wiki = self.model(name=page, creator=request.user, modified_user=request.user)
            
            conflict = False
            #check if there is someone is changing the wiki page
            if wiki.start_time and (date.now() - wiki.start_time).seconds < settings.get_var('WIKI/WIKI_EDIT_CHECK_TIMEDELTA') and wiki._cur_user_ != request.user.id:
                conflict = True
            else:
                #record user and edit begin time
                wiki.cur_user = request.user.id
                wiki.start_time = date.now()
                
            wiki.save()
            
            data = wiki.to_dict()
            data['name'] = page.rsplit('/', 1)[-1]
            form.bind(data)
            
            return {'form':form, 'wiki':wiki, 'conflict':conflict}
        
        elif request.method == 'POST':
            form.wiki = wiki
            form.parent = parent
            if form.validate(request.POST):
                #check admin permission
                old_acl, old_acl_lines, old_begin = find_acl(wiki.acl, settings.WIKI_ACL_ALIAS)
                acl, acl_lines, begin = find_acl(form.content.data, settings.WIKI_ACL_ALIAS)
                if old_acl_lines != acl_lines:
                    if not self._check_permission('admin', old_acl, raise_exception=False, page=wiki):
                        flash(_('You have no right to change the acl info.'), 'error')
                    else:
                        wiki.acl = acl_lines
                lines = form.content.data.rstrip().splitlines()
                if wiki.acl:
                    wiki.content = '\n'.join([wiki.acl] + lines[begin:])
                else:
                    wiki.content = '\n'.join(lines[begin:])
                wiki.modified_user = request.user.id
                wiki.modified_time = date.now()
                wiki.name = form.name.data
                if parent:
                    wiki.name = parent + '/' + form.name.data
                    
                #check if there is already same named page existed
                page = self.model.get((self.model.c.name==wiki.name) & (self.model.c.id != wiki.id))
                if page:
                    if not page.enabled or page.deleted:
                        self._delete_wikipage(page, real=True)

                wiki.subject = form.subject.data or ''
                wiki.enabled = True
                
                #process cur_user and start_time, clear when the cur_user is
                #request.user
                if wiki._cur_user_ and wiki._cur_user_ == request.user.id:
                    wiki.cur_user = None
                    wiki.start_time= None
                    
                wiki.save()
                wiki.new_revision()
                
                #enable attachments
                enable_attachments(None, wiki, wiki.id)
                
                #update cached page
                self._get_cached_page_html(wiki.name, wiki.content, update=True)
                
                return redirect(url_for(self.__class__.wiki, pagename=wiki.name))
            else:
                conflict = False
                #check if there is someone is changing the wiki page
                if wiki.start_time and (date.now() - wiki.start_time).seconds < settings.get_var('WIKI/WIKI_EDIT_CHECK_TIMEDELTA') and wiki._cur_user_ != request.user.id:
                    conflict = True
                return {'form':form, 'wiki':wiki, 'conflict':conflict}
            
    def _wiki_update_editor(self, pagename):
        """
        更新当前页面的编辑用户及时间
        """
        wiki = self.model.get(self.model.c.name == pagename)
        if wiki:
            #check read permission
            self._check_permission('edit', wiki, page=wiki)
            
            wiki.cur_user = request.user.id
            wiki.start_time = date.now()
            wiki.save()
            return json({'success':True})
        else:
            return json({'success':False, 'message':'页面不存在'})
            
    def _delete_wikipage(self, wiki, real=False):
        """
        real 表示是否真正删除
        """
        self.changeset.filter(self.changeset.c.wiki == wiki.id).remove()
        Attachments = functions.get_model('generic_attachment')
        
        #删除附件
        Attachments.delete_files(wiki)
        #删除缓存文件
        self._del_cached_page_html(wiki.name)
        
        if real:
            delete_fieldname = None
        else:
            delete_fieldname = 'deleted'
        wiki.delete(delete_fieldname=delete_fieldname)
        
    def _wiki_delete(self, pagename):
        from uliweb import request
        
        wiki = self.model.get(self.model.c.name == pagename)
        if wiki:
            #check read permission
            self._check_permission('delete', wiki, page=wiki)
            #delete wiki page
            self._delete_wikipage(wiki)
            return redirect(url_for(self.__class__.wiki))
        else:
            error("The page %s is not existed, please check!" % pagename)
        
    def _wiki_revision(self, pagename):
        from uliweb import request, response
        
        response.template = 'WikiView/wiki_revision.html'
        
        wiki = self.model.get(self.model.c.name == pagename)
        if wiki:
            return {'wiki':wiki, 'can_revert':self._check_permission('revert', wiki.acl, page=wiki, raise_exception=False)}
        else:
            error(unicode(_("The page %s is not existed, please check!")) % pagename)
        
    def _wiki_get_revision(self, pagename):
        from uliweb import request, json
        
        page = int(request.GET.get('page', 1))
        num = settings.WIKI.WIKI_REVISION_NUM
        
        wiki = self.model.get(self.model.c.name == pagename)
        if wiki:
            count = wiki.changeset.all().count()
            changeset = wiki.changeset.all().fields('wiki', 'revision', 'editor', 'modified_time').order_by(self.changeset.c.revision.desc()).limit(num).offset((page-1)*num)
            result = []
            for row in changeset:
                d = row.to_dict(fields=['wiki', 'revision', 'editor', 'modified_time'])
                d['editor'] = unicode(row.editor)
                result.append(d)
                
            return json({'success':True, 'changeset':result, 'next':(page)*num<count})
        else:
            return json({'success':False, 'message':unicode(_("The page %s is not existed, please check!")) % pagename})
            
    def _wiki_diff(self, pagename):
        from uliweb import request, response
        from diff2html import diff2html

        response.template = 'WikiView/wiki_diff.html'
        
        rev1 = int(request.GET['rev1'])
        rev2 = int(request.GET['rev2'])
        
        wiki = self.model.get(self.model.c.name == pagename)
        
        #check read permission
        self._check_permission('read', wiki, page=wiki)

        c1 = self.changeset.get((self.changeset.c.wiki == wiki.id) & (self.changeset.c.revision==rev1))
        c2 = self.changeset.get((self.changeset.c.wiki == wiki.id) & (self.changeset.c.revision==rev2))

        def _create(content1, content2, name):
            content = self._diff(content1, content2)
            fileinfo = '%s <a href="%s">r%d</a> - <a href="%s">r%d</a>' % (name,
                url_for(self.__class__.wiki, pagename=pagename, rev=rev2),
                rev2,
                url_for(self.__class__.wiki, pagename=pagename, rev=rev1),
                rev1,
                )
            return diff2html(pagename, pagename, content, fileinfo=fileinfo)
        content_diff = _create(c1.old_content, c2.old_content, pagename)
        subject_diff = _create(c1.old_subject, c2.old_subject, pagename)
        attachments_diff = _create(c1.old_attachments, c2.old_attachments, pagename)
        return {'content':content_diff, 
            'subject_content':subject_diff,
            'attachments_content':attachments_diff,
            'wiki':wiki}

    def _diff(self, txt1, txt2):
        from difflib import unified_diff
        
        return unified_diff(txt1.splitlines(), txt2.splitlines())

    def _wiki_revert(self, pagename):
        from uliweb import request
        
        wiki = self.model.get(self.model.c.name == pagename)
        
        #check read permission
        self._check_permission('revert', wiki, page=wiki)
        
        rev = int(request.GET['rev'])
        r = self.changeset.get((self.changeset.c.wiki==wiki.id) & (self.changeset.c.revision==rev))
        if (wiki.content != r.old_content or wiki.subject != r.old_subject) :
            wiki.content = r.old_content
            wiki.subject = r.old_subject
            wiki.modified_user = request.user
            wiki.modified_time = date.now()
            wiki.save()
            wiki.new_revision()
        
        #update cached page
        self._get_cached_page_html(wiki.name, wiki.content, update=True)
        
        return redirect(url_for(self.__class__.wiki, pagename=pagename))
        
    def _wiki_test_acl(self, pagename):
        from uliweb import request
        
        User = functions.get_model('user')
        user = User.get(User.c.username == request.POST.get('username'))
        
        wiki = self.model.get(self.model.c.name == pagename)
        wiki.acl = request.POST.get('acl')
        p = ['read', 'write', 'revert', 'delete', 'admin']
        
        result = self._find_tree_permissions(p, wiki, user)
        
        x = [(y, result.get(y)) for y in p]
        
        return json({'success':True, 'data':x})
    
    def _wiki_code(self, pagename):
        from uliweb import request
        
        response.template = 'WikiView/wiki_code.html'
        wiki = self.model.get(self.model.c.name == pagename)
        return {'wiki':wiki}
        