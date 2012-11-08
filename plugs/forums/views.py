#coding=utf-8
import os
from uliweb import expose, decorators, functions
from uliweb.orm import get_model, do_
from datetime import timedelta
from uliweb.utils.common import safe_str
from uliweb.utils import date
from uliweb.utils.timesince import timesince
import uuid

#def __begin__():
#   from uliweb import function
#   return function('require_login')()

def convert_managers(value, obj):
    r = dict([(m.id,unicode(m)) for m in obj.managers])
    return r

@expose('/forum')
class ForumView(object):
    def __init__(self):
        self.status = {
            'close':{True:'打开', False:'关闭'},
            'sticky':{True:'取消顶置', False:'顶置'},
            'essence':{True:'取消精华', False:'精华'},
            'delete':{True:'恢复', False:'删除'},
            'hidden':{True:'取消隐藏', False:'隐藏'},
            'email':{True:'取消邮件关注', False:'设置邮件关注'},
            'homepage':{True:'取消首页显示', False:'设置首页显示'},
        }
        self.model = get_model('forum')
    
    @expose('')
    def list(self):
        """
        显示论坛列表
        """
        category = get_model('forumcategory')
        return {'categories':category.all().order_by(category.c.ordering), 'count':category.count()}
    
    @decorators.check_role('superuser')
    def admin(self):
        """
        显示管理页面
        """
        return {}
    
    @expose('admin/categories')
    @decorators.check_role('superuser')
    def admin_categories(self):
        """
        返回版块信息
        """
        from uliweb.utils.generic import ListView
        
        def ordering(value, obj):
            return obj.ordering
        
        view = ListView('forumcategory', pagination=False, fields_convert_map={'ordering':ordering})
        return json(view.json())
    
    @expose('admin/categories/add')
    @decorators.check_role('superuser')
    def admin_categories_add(self):
        from uliweb.utils.generic import AddView
        view = AddView('forumcategory', success_data=True)
        return view.run(json_result=True)
        
    @expose('admin/categories/edit/<id>')
    @decorators.check_role('superuser')
    def admin_categories_edit(self, id):
        """
        修改板块
        """
        from uliweb.utils.generic import EditView
        
        category = get_model('forumcategory')
        obj = category.get(int(id))
        view = EditView(category, obj=obj, success_data=True)
        return view.run(json_result=True)
    
    @expose('admin/categories/delete/<id>')
    @decorators.check_role('superuser')
    def admin_categories_delete(self, id):
        """
        删除板块
        """
        from uliweb.utils.generic import DeleteView
        
        category = get_model('forumcategory')
        
        obj = category.get(int(id))
        
        def validator(obj):
            if obj.forums.all().count() > 0:
                return u"[%s]板块下还存在论坛，请先将论坛删除或转移至其它的板块后再删除" % obj.name
        
        view = DeleteView(category, obj=obj, validator=validator)
        return view.run(json_result=True)

    @expose('admin/forums')
    @decorators.check_role('superuser')
    def admin_forum(self):
        """
        显示管理论坛页面
        """
        cat = request.GET.get('category_id', 0)
        Category = get_model('forumcategory')
        obj = Category.get(int(cat))
        return {'category':obj}
        
    @expose('admin/forums/query')
    @decorators.check_role('superuser')
    def admin_forum_query(self):
        """
        显示管理论坛页面
        """
        from uliweb.utils.generic import ListView
        
        cat = request.GET.get('category_id', 0)
        condition = self.model.c.category == int(cat)
        
        def ordering(value, obj):
            return obj.ordering
        
        def topictype(value, obj):
            return dict([(x.id,unicode(x)) for x in obj.forum_topictypes.all()])
        
        view = ListView(self.model, pagination=False, condition=condition,
            fields_convert_map={'managers':convert_managers, 
                'ordering':ordering,
                'topictype':topictype})
        return json(view.json())
    
    @expose('admin/forums/add')
    @decorators.check_role('superuser')
    def admin_forum_add(self):
        """
        添加新的论坛
        """
        from uliweb.utils.generic import AddView, get_field_display
        
        def post_created_form(fcls, model):
            fcls.managers.choices = [('', '')]

        def success_data(obj, data):
            d = obj.to_dict()
            d['managers'] = convert_managers(None, obj)
            return d
        
        view = AddView(self.model, 
            success_data=success_data,
            post_created_form=post_created_form,
            default_data={'category':request.GET.get('category')},
        )
        return view.run(json_result=True)
    
    @expose('admin/forums/edit/<id>')
    @decorators.check_role('superuser')
    def admin_forum_edit(self, id):
        """
        修改论坛
        """
        from uliweb.utils.generic import EditView
        
        forum = get_model('forum')
    
        obj = forum.get(int(id))
        
        def post_created_form(fcls, model, obj):
            fcls.managers.query = obj.managers

        def success_data(obj, data):
            d = obj.to_dict()
            d['managers'] = convert_managers(None, obj)
            return d
        
        view = EditView(self.model, obj=obj,
            success_data=success_data,
            post_created_form=post_created_form,
            )
        return view.run(json_result=True)
    
    @expose('admin/forums/delete/<id>')
    @decorators.check_role('superuser')
    def forum_delete(self, id):
        """
        删除论坛
        """
        from uliweb.utils.generic import DeleteView
        
        forum = get_model('forum')
        
        obj = forum.get(int(id))
        
        def validator(obj):
            if obj.forum_topics.all().count() > 0:
                return u"[%s]论坛下还存在发贴，请先将发贴删除或转移至其它的论坛后再删除" % obj.name
        
        view = DeleteView(forum, url_for(ForumView.admin_forum), 
            url_for(ForumView.admin_forum),
            obj=obj, validator=validator)
        return view.run(json_result=True)
    
    @expose('admin/forums/topictype/add')
    @decorators.check_role('superuser')
    def forumtopictype_add(self):
        """
        添加新的论坛
        """
        from uliweb.utils.generic import AddView
        
        forum_id = int(request.POST.get('forum_id'))

        view = AddView('forumtopictype', success_data=True, 
            default_data={'forum':forum_id})
        return view.run(json_result=True)
    
    @expose('admin/forums/topictype/edit/<id>')
    @decorators.check_role('superuser')
    def forumtopictype_edit(self, id):
        """
        修改论坛
        """
        from uliweb.utils.generic import EditView
        
        forumtopictype = get_model('forumtopictype')
    
        obj = forumtopictype.get(int(id))
        
        view = EditView('forumtopictype', obj=obj, success_data=True)
        return view.run(json_result=True)
    
    @expose('admin/forums/topictype/delete/<id>')
    @decorators.check_role('superuser')
    def forumtopictype_delete(self, id):
        """
        删除论坛
        """
        from uliweb.utils.generic import DeleteView
        
        forumtopictype = get_model('forumtopictype')
        
        obj = forumtopictype.get(int(id))
        
        def validator(obj):
            forumtopic = get_model('forumtopic')
            if forumtopic.filter(forumtopic.c.topic_type==int(id)).count() > 0:
                return u"存在此主题类型的贴子，请先将此类型的贴子改为其它的类型后再删除"
        
        view = DeleteView(forumtopictype,
            obj=obj, validator=validator)
        return view.run(json_result=True)

    @expose('<int:id>')
    def forum_index(self, id):
        """
        显示某论坛页面
        """
        from uliweb.utils.generic import ListView
        from sqlalchemy.sql import and_
        import math
        
        pageno = int(request.values.get('page', 1)) - 1
        rows_per_page=int(request.values.get('rows', settings.get_var('PARA/FORUM_INDEX_NUMS')))
        
        Topic = get_model('forumtopic')
        Forum = get_model('forum')
        User = get_model('user')
        forum = Forum.get(int(id))
        condition = Topic.c.forum == int(id)
        order_by = [Topic.c.sticky.desc(), Topic.c.last_reply_on.desc()]
        if not forum.managers.has(request.user):
            condition = (Topic.c.hidden==False) & condition
        
        filter = request.GET.get('filter', 'all')
        if filter == 'essence':
            condition = (Topic.c.essence==True) & condition
        elif filter == 'sticky':
            condition = (Topic.c.sticky==True) & condition
        term = request.GET.get('term', '')
        type = request.GET.get('type', '1')
        if term:
            if type == '1':     #查找主题
                condition = (Topic.c.subject.like('%'+term+'%')) & condition
            elif type == '2':   #查找用户名
                condition = and_(Topic.c.posted_by == User.c.id,
                    User.c.username.like('%' + term + '%') | User.c.nickname.like('%' + term + '%'),
                    ) & condition
            
        def created_on(value, obj):
            return value.strftime('%Y-%m-%d')
        
        def last_reply_on(value, obj):
            return timesince(value)
        
        def subject(value, obj):
            if obj.topic_type:
                _type = u'[%s]' % obj.get_display_value('topic_type')
            else:
                _type = ''
            s = ''
            if obj.sticky:
                s += u'<font color="red">[顶]</font>'
            if obj.hidden:
                s += u'<font color="red">[隐]</font>'
            if obj.closed:
                s += u'<font color="red">[关]</font>'
            if obj.essence:
                s += u'<font color="red">[精]</font>'
            if obj.homepage:
                s += u'<font color="red">[首]</font>'
            return _type+ '<a href="/forum/%d/%d">%s</a>' % (int(id), obj.id, obj.subject) + s
        
        fields_convert_map = {'created_on':created_on, 'subject':subject,
            'last_reply_on':last_reply_on}
        view = ListView(Topic, condition=condition, order_by=order_by,
            rows_per_page=rows_per_page, pageno=pageno,
            fields_convert_map=fields_convert_map)
        view.query()    #in order to get the total count
        objects = view.objects()
        pages = int(math.ceil(1.0*view.total/rows_per_page))
        return {'forum':forum, 'objects':objects, 'filter':filter, 'term':term, 
            'page':pageno+1, 'total':view.total, 'pages':pages,
            'pagination':functions.create_pagination(request.url, view.total, pageno+1, rows_per_page),
            'type':type, 'filter_name':dict(settings.get_var('PARA/FILTERS')).get(filter)}
#        if 'data' in request.values:
#            return json(view.json())
#        else:
#            return {'forum':forum, 'filter':filter, 'term':term, 'type':type, 'page':pageno+1,
#                'filter_name':dict(settings.get_var('PARA/FILTERS')).get(filter)}
    
    @expose('<int:id>/new_topic')
    @decorators.check_role('trusted')
    def new_topic(self, id):
        """
        发表新主题
        """
        from uliweb.utils.generic import AddView
        
        Forum = get_model('forum')
        forum = Forum.get(int(id))
        
        def post_save(obj, data):
            from sqlalchemy.sql import select, func
            Post = get_model('forumpost')
            
            p = Post(topic=obj.id, posted_by=request.user, slug=obj.slug,
                content=data['content'], floor=1, reply_email=data['reply_email'])
            p.save()
            
            obj.last_post = p.id
            obj.save()
            
            Forum.filter(Forum.c.id==int(id)).update(num_posts=Forum.c.num_posts+1, 
                num_topics=Forum.c.num_topics+1,
                last_post_user=request.user.id, last_reply_on=date.now(), last_post=p.id)
            #根据slug的值清除附件中无效的文件
            self._clear_files(obj.slug, data['content'])
            
        def get_form_field(name):
            from uliweb.utils.generic import ReferenceSelectField
            from uliweb.form import TextField, BooleanField
            
            forumtopictype = get_model('forumtopictype')
            
            if name == 'content':
                return TextField('内容', required=True, convert_html=True)
            elif name == 'topic_type':
                return ReferenceSelectField('forumtopictype', 
                    condition=forumtopictype.c.forum==forum.id, label='主题分类名称')
            elif name == 'reply_email':
                return BooleanField('有回复时邮件通知我')
            
        slug = uuid.uuid1().hex
        data = {'slug':slug, 'reply_email':False}
        
        has_email = bool(request.user and request.user.email)
        
        view = AddView('forumtopic', url_for(ForumView.forum_index, id=int(id)),
            default_data={'forum':int(id), 'last_post_user':request.user.id, 'last_reply_on':date.now()}, 
            hidden_fields=['slug'], data=data,
            post_save=post_save, get_form_field=get_form_field, template_data={'forum':forum, 'has_email':has_email, 'slug':slug})
        return view.run()
        
    def _clear_files(self, slug, text):
        import re
        import itertools
        from uliweb.utils.image import fix_filename
        File = get_model('forumattachment')
        
        r_links = re.compile(r'<a.*?href=\"([^"\?]+)(?:\"|\?)|<img.*?src=\"([^"]+)\"|<embed.*?src=\"([^"]+)\"', re.DOTALL)
        files = filter(None, itertools.chain(*re.findall(r_links, text)))
        for row in File.filter(File.c.slug==slug):
            _f = functions.get_filename(row.file_name)
            url = functions.get_href(row.file_name)
            if url in files:
                row.enabled = True
                row.save()
            else:
                if os.path.exists(_f):
                    os.unlink(_f)
                thumbnail = fix_filename(_f, '.thumbnail')
                if os.path.exists(thumbnail):
                    os.unlink(thumbnail)
                
        File.filter(File.c.slug==slug).filter(File.c.enabled==False).remove()
    
    @expose('<int:forum_id>/<int:topic_id>')
    def topic_view(self, forum_id, topic_id):
        """
        显示某主题页面
        """
        from uliweb.utils.generic import ListView
        from uliweb import settings
        
        pageno = int(request.values.get('page', 1)) - 1
        rows_per_page=int(request.values.get('rows', settings.get_var('PARA/FORUM_PAGE_NUMS')))
        
        Post = get_model('forumpost')
        Topic = get_model('forumtopic')
        Forum = get_model('forum')
        forum = Forum.get(int(forum_id))
        condition = Post.c.topic == int(topic_id)
        condition1 = (Post.c.parent == None) & condition
        condition2 = (Post.c.parent != None) & condition
        order_by = [Post.c.floor]
        
        def created_on(value, obj):
            return date.to_local(value).strftime('%Y-%m-%d %H:%M:%S %Z')
        
        def content(value, obj):
            if obj.deleted:
                return u'<div class="deleted">内容已经被 %s 于时间 %s 删除 </div>' % (obj.deleted_by.username, obj.field_str(obj.deleted_on))
            else:
                return value
        
        def username(value, obj):
            return obj.posted_by.username
        
        def userimage(value, obj):
            get_user_image = function('get_user_image')
            url = get_user_image(obj.posted_by)
            return url
        
        def actions(value, obj):
            if not request.user:
                return ''
            
            a = []
            is_manager = forum.managers.has(request.user)
            if obj.floor == 1 and obj.parent == None:
                #第一楼为主贴，可以允许关闭，顶置等操作
                if is_manager:
                    a.append('<a href="#" rel="%d" class="close">%s</a>' % (obj.id, self.status['close'][obj.topic.closed]))
                    a.append('<a href="#" rel="%d" class="hidden">%s</a>' % (obj.id, self.status['hidden'][obj.topic.hidden]))
                    a.append('<a href="#" rel="%d" class="top">%s</a>' % (obj.id, self.status['sticky'][obj.topic.sticky]))
                    a.append('<a href="#" rel="%d" class="essence">%s</a>' % (obj.id, self.status['essence'][obj.topic.essence]))
                    a.append('<a href="#" rel="%d" class="homepage">%s</a>' % (obj.id, self.status['homepage'][obj.topic.homepage]))
                if is_manager or (obj.posted_by.id == request.user.id and obj.created_on+timedelta(days=settings.get_var('PARA/FORUM_EDIT_DELAY'))>=date.now()):
                    #作者或管理员且在n天之内，则可以编辑
                    url = url_for(ForumView.edit_topic, forum_id=forum_id, topic_id=topic_id)
                    a.append('<a href="%s" rel="%d" class="edit">编辑</a>' % (url, obj.id))
                if is_manager:
                    url = url_for(ForumView.remove_topic, forum_id=forum_id, topic_id=topic_id)
                    a.append('<a href="%s" rel="%d" class="delete_topic">删除主题</a>' % (url, obj.id))
            if is_manager or (obj.posted_by.id == request.user.id):
                if (obj.deleted and (obj.deleted_by.id == request.user.id or is_manager)) or not obj.deleted:
                    a.append('<a href="#" rel="%d" class="delete">%s</a>' % (obj.id, self.status['delete'][obj.deleted]))
            if obj.posted_by.id == request.user.id:    
                a.append('<a href="#" rel="%d" class="email">%s</a>' % (obj.id, self.status['email'][obj.reply_email]))
            a.append('<a href="/forum/%d/%d/%d/new_reply">回复该作者</a>' % (forum_id, topic_id, obj.id))
            return ' | '.join(a)
        
        def updated(value, obj):
            if obj.floor == 1 and obj.topic.updated_on and not obj.parent:
                return u'<div class="updated">由 %s 于 %s 更新</div>' % (obj.topic.modified_user.username, timesince(obj.topic.updated_on))
        
        fields = ['topic', 'id', 'username', 'userimage', 'posted_by', 'content',
            'created_on', 'actions', 'floor', 'updated', 'parent',
            ]
        fields_convert_map = {'created_on':created_on, 'content':content,
            'username':username, 'userimage':userimage, 'actions':actions,
            'updated':updated}
        #view1 为生成一级回复，即回复主题
        view1 = ListView(Post, fields=fields, condition=condition1, order_by=order_by,
            rows_per_page=rows_per_page, pageno=pageno,
            fields_convert_map=fields_convert_map)
        #view2 为生成二级乃至多级回复
        view2 = ListView(Post, fields=fields, condition=condition2, order_by=order_by,
            pagination=False,
            fields_convert_map=fields_convert_map)
        key = '__topicvisited__:forumtopic:%s:%s:%s' % (request.remote_addr, forum_id, topic_id)
        cache = function('get_cache')()
        v = cache.get(key, None)
        if not v:
            Topic.filter(Topic.c.id==int(topic_id)).update(num_views=Topic.c.num_views+1)
            cache.set(key, 1, settings.get_var('PARA/FORUM_USER_VISITED_TIMEOUT'))
        
        slug = uuid.uuid1().hex
        topic = Topic.get(int(topic_id))
        
        #处理posts和sub_posts
        query = view1.query()
        posts = []
        sub_posts = {}
        def process_sub(ids):
            _ids = []
            for x in Post.filter(Post.c.parent.in_(ids)).order_by(Post.c.floor):
                obj = view2.object(x)
                d = sub_posts.setdefault(str(x._parent_), [])
                d.append(obj)
                _ids.append(x.id)
            if _ids:
                process_sub(_ids)
                
        ids = []
        for row in query:
            posts.append(view1.object(row))
            ids.append(row.id)
            
        process_sub(ids)
           
        pagination = functions.create_pagination(request.url, view1.total,
            pageno+1, rows_per_page)
        return {'forum':forum, 'topic':topic, 'slug':slug, 
            'has_email':bool(request.user and request.user.email), 
            'page':pageno+1, 'pagination':pagination,
            'posts':posts, 'sub_posts':sub_posts}
#        if 'data' in request.values:
#            return json({'post1':view1.json(),'post2':view2.json()})
#        else:
##            key = '__topicvisited__:forumtopic:%d:%s:%s' % (request.user.id, forum_id, topic_id)
#            key = '__topicvisited__:forumtopic:%s:%s:%s' % (request.remote_addr, forum_id, topic_id)
#            cache = function('get_cache')()
#            v = cache.get(key, None)
#            if not v:
#                Topic.filter(Topic.c.id==int(topic_id)).update(num_views=Topic.c.num_views+1)
#                cache.set(key, 1, settings.get_var('PARA/FORUM_USER_VISITED_TIMEOUT'))
#
#            slug = uuid.uuid1().hex
#            topic = Topic.get(int(topic_id))
#            return {'forum':forum, 'topic':topic, 'slug':slug, 'has_email':bool(request.user and request.user.email), 'page':pageno+1}
    
    @expose('<forum_id>/<topic_id>/new_post')
    @decorators.check_role('trusted')
    def new_post(self, forum_id, topic_id):
        """
        发表新回复
        """
        from uliweb.utils.generic import AddView
        
        Post = get_model('forumpost')
        Topic = get_model('forumtopic')
        Forum = get_model('forum')
        User = get_model('user')

        def pre_save(data):
            from sqlalchemy.sql import select, func

            data['topic'] = int(topic_id)
            data['floor'] = (do_(select([func.max(Post.c.floor)], Post.c.topic==int(topic_id))).scalar() or 0) + 1
            
        def post_save(obj, data):
            from uliweb import functions
            from uliweb.utils.common import Serial
            from uliweb.mail import Mail
            
            Topic.filter(Topic.c.id==int(topic_id)).update(
                num_replies=Topic.c.num_replies+1, 
                last_post_user=request.user.id, 
                last_reply_on=date.now(),
                last_post=obj.id)
            Forum.filter(Forum.c.id==int(forum_id)).update(
                num_posts=Forum.c.num_posts+1, 
                last_post_user=request.user.id, 
                last_reply_on=date.now(),
                last_post=obj.id)
            self._clear_files(obj.slug, data['content'])
            
            #増加发送邮件的处理
            emails = []
            for u_id in Post.filter((Post.c.topic==int(topic_id)) & (Post.c.reply_email==True) & (Post.c.floor<obj.floor)).values(Post.c.posted_by):
                user = User.get(u_id[0])
                if user and user.email and (user.email not in emails) and (user.email!=request.user.email):
                    emails.append(user.email)
            
            if not emails:
                return
            
            _type = settings.get_var('PARA/FORUM_REPLY_PROCESS', 'print')
            url = '%s/forum/%s/%s' % (settings.get_var('PARA/DOMAIN'), forum_id, topic_id)
            d = {'url':str(url)}
            mail = {'from_':settings.get_var('PARA/EMAIL_SENDER'), 'to_':emails,
                'subject':settings.get_var('FORUM_EMAIL/FORUM_EMAIL_TITLE'),
                'message':settings.get_var('FORUM_EMAIL/FORUM_EMAIL_TEXT') % d,
                'html':True}
            
            if _type == 'mail':
                Mail().send_mail(**mail)
            elif _type == 'noprint':
                pass
            elif _type == 'print':
                print mail
            elif _type == 'redis':
                redis = functions.get_redis()
                _t = Serial.dump(mail)
                redis.lpush('send_mails', _t)
            
        def get_form_field(name):
            from uliweb.form import TextField
            if name == 'content':
                return TextField('内容', required=True, convert_html=True, rows=20)
        
        slug = uuid.uuid1().hex
        data = {'slug':slug, 'reply_email':False, 'content':''}

        def success_data(obj, data):
            import math
            
            return {'page':int(math.ceil(1.0*obj.floor/settings.get_var('PARA/FORUM_PAGE_NUMS')))}
        
        view = AddView('forumpost', url_for(ForumView.topic_view, forum_id=int(forum_id), topic_id=int(topic_id)),
            hidden_fields=['slug'], template_data={'slug':slug}, data=data,
            success_data=success_data,
            pre_save=pre_save, get_form_field=get_form_field, post_save=post_save)
        return view.run(json_result=True)
    
    @expose('<forum_id>/<topic_id>/<parent_id>/new_reply')
    @decorators.check_role('trusted')
    def new_reply(self, forum_id, topic_id, parent_id):
        """
        发表新回复
        """
        from uliweb.utils.generic import AddView
        
        Forum = get_model('forum')
        forum = Forum.get(int(forum_id))
        Topic = get_model('forumtopic')
        topic = Topic.get(int(topic_id))
        Post = get_model('forumpost')
        post = Post.get(int(parent_id))
        User = get_model('user')
    
        def pre_save(data):
            from sqlalchemy.sql import select, func
    
            data['topic'] = int(topic_id)
            data['parent'] = int(parent_id)
            data['floor'] = (do_(select([func.max(Post.c.floor)], Post.c.parent==post.id)).scalar() or 0) + 1
            
        def post_save(obj, data):
            from uliweb import functions
            from uliweb.utils.common import Serial
            from uliweb.mail import Mail
            
            Post.filter(Post.c.id==int(parent_id)).update(num_replies=Post.c.num_replies+1, last_post_user=request.user.id, last_reply_on=date.now())            
            self._clear_files(obj.slug, data['content'])
            
            Topic.filter(Topic.c.id==int(topic_id)).update(
                num_replies=Topic.c.num_replies+1, 
                last_post_user=request.user.id, 
                last_reply_on=date.now(),
                last_post=obj.id)
            Forum.filter(Forum.c.id==int(forum_id)).update(
                num_posts=Forum.c.num_posts+1, 
                last_post_user=request.user.id, 
                last_reply_on=date.now(),
                last_post=obj.id)
            
            #増加发送邮件的处理
            emails = []
            for u_id in Post.filter((Post.c.topic==int(topic_id)) & (Post.c.reply_email==True) & (Post.c.id==parent_id)).values(Post.c.posted_by):
                user = User.get(u_id[0])
                if user and user.email and (user.email not in emails) and (user.email!=request.user.email):
                    emails.append(user.email)
            
            if not emails:
                return
            
            _type = settings.get_var('PARA/FORUM_REPLY_PROCESS', 'print')
            url = '%s/forum/%s/%s' % (settings.get_var('PARA/DOMAIN'), forum_id, topic_id)
            d = {'url':str(url)}
            mail = {'from_':settings.get_var('PARA/EMAIL_SENDER'), 'to_':emails,
                'subject':settings.get_var('FORUM_EMAIL/FORUM_EMAIL_TITLE'),
                'message':settings.get_var('FORUM_EMAIL/FORUM_EMAIL_TEXT') % d,
                'html':True}
            
            if _type == 'mail':
                Mail().send_mail(**mail)
            elif _type == 'print':
                print mail
            elif _type == 'redis':
                redis = functions.get_redis()
                _t = Serial.dump(mail)
                redis.lpush('send_mails', _t)
            
        def get_form_field(name):
            from uliweb.form import TextField
            if name == 'content':
                return TextField('内容',required=True, convert_html=True, default='')

        slug = uuid.uuid1().hex
        data = {'slug':slug, 'reply_email':False, 'content':_('RE')+ ' @'+unicode(post.posted_by)+': '}
        has_email = bool(request.user and request.user.email)
        view = AddView('forumpost', 
            url_for(ForumView.topic_view, forum_id=int(forum_id), topic_id=int(topic_id)),
#            default_data={'last_post_user':request.user.id, 'last_reply_on':date.now()}, 
            hidden_fields=['slug'], data=data,
            pre_save=pre_save, 
            get_form_field=get_form_field, 
            post_save=post_save,
            template_data={'forum':forum, 'topic':topic, 'has_email':has_email, 'slug':slug})
        return view.run()

    @expose('<forum_id>/<topic_id>/edit_topic')
    @decorators.check_role('trusted')
    def edit_topic(self, forum_id, topic_id):
        """
        修改主题
        """
        from uliweb.utils.generic import EditView
        
        Forum = get_model('forum')
        forum = Forum.get(int(forum_id))
        Topic = get_model('forumtopic')
        topic = Topic.get(int(topic_id))
        Post = get_model('forumpost')
        post = Post.get((Post.c.topic==int(topic_id)) & (Post.c.floor==1))
        
        #compatiable not saving the first post slug bug
        if not post.slug:
            post.slug = uuid.uuid1().hex
            post.save()
        
        def post_save(obj, data):
            #更新Post表
            post.content = data['content']
            post.save()
            
            self._clear_files(obj.slug, data['content'])
            
        def pre_save(obj, data):
            flag = False
            if data['topic_type'] != obj.topic_type:
                flag = True
            if not flag and data['subject'] != obj.subject:
                flag = True
            if not flag and data['content'] != safe_str(post.content):
                flag = True
            if flag:
                data['modified_user'] = request.user.id
                data['updated_on'] = date.now()
            
        def get_form_field(name, obj):
            from uliweb.form import TextField
            if name == 'content':
                return TextField('内容', required=True, rows=20, convert_html=True)
        
        data = {'content':post.content}
        view = EditView('forumtopic', url_for(ForumView.topic_view, forum_id=forum_id, topic_id=topic_id),
            obj=topic, data=data, pre_save=pre_save, hidden_fields=['slug'],
            post_save=post_save, get_form_field=get_form_field, template_data={'forum':forum, 'topic':topic, 'slug':post.slug})
        return view.run()
    
    def upload_file(self):
        return self._upload_file(image=False, show_filename=True)
    
    def upload_image(self):
        return self._upload_file(image=True)

    def _upload_file(self, image=False, show_filename=True):
        import os
        import Image
        if image:
            from forms import ImageUploadForm as Form
        else:
            from forms import FileUploadForm as Form
        from uliweb.utils.image import thumbnail_image, fix_filename
        from uliweb import json_dumps
        
        File = get_model('forumattachment')
        
        forum_id = request.GET.get('forum_id')
        slug = request.GET.get('slug')
        form = Form()
        suffix = date.now().strftime('_%Y_%m_%d')
        if request.method == 'GET':
            form.bind({'is_thumbnail':True})
            return {'form':form}
        else:
            flag = form.validate(request.values, request.files)
            if flag:
                f = form.data['filedata']
                _f = os.path.basename(f['filename'])
                #文件格式为forum/<forum_id>/<filename_yyyy_mm_dd>
                filename = fix_filename('forum/%s/%s' % (forum_id, _f), suffix)
                if image:
                    filename = functions.save_file(filename, f['file'])
                    if form.data['is_thumbnail']:
                        #process thumbnail
                        rfilename, thumbnail = thumbnail_image(functions.get_filename(filename, filesystem=True), filename, settings.get_var('PARA/FORUM_THUMBNAIL_SIZE'))
                        _file = functions.get_href(thumbnail)
                    else:
                        _file = functions.get_href(filename)
                    name = functions.get_href(filename)
                else:
                    filename = functions.save_file(filename, f['file'])
                    name = form.data['title']
                    if not name:
                        name = _f
                    _file = functions.get_href(filename, alt=name)
                ff = File(slug=slug, file_name=filename, name=name)
                ff.save()
                name = json_dumps(name, unicode=True)
                if show_filename:
                    fargs = '||%s' % name[1:-1]
                else:
                    fargs = ''
                return '''<script type="text/javascript">
var url='%s%s';
setTimeout(function(){callback(url);},100);
</script>
''' % (_file, fargs)
            else:
                return {'form':form}
                
    @expose('<forum_id>/<topic_id>/remove_topic')
    @decorators.check_role('trusted')
    def remove_topic(self, forum_id, topic_id):
        from sqlalchemy.sql import select
        
        Forum = get_model('forum')
        forum = Forum.get(int(forum_id))
        Topic = get_model('forumtopic')
        topic = Topic.get(int(topic_id))
        Post = get_model('forumpost')
        post = Post.get((Post.c.topic==int(topic_id)) & (Post.c.floor==1))
        FA = get_model('forumattachment')
        
        if not topic:
            error("主题已经不存在的")
            
        is_manager = post.topic.forum.managers.has(request.user)
        if is_manager:
            query = FA.filter(FA.c.slug==Post.c.slug).filter(Post.c.topic==int(topic_id))
            #删除相应附件
            for a in query:
                functions.delete_filename(a.file_name)
            #删除FA记录
            FA.filter(FA.c.slug.in_(select([Post.c.slug], Post.c.topic==int(topic_id)))).remove()
            #删除所有POST
            post_query = Post.filter(Post.c.topic==int(topic_id))
            post_count = post_query.count()
            post_query.remove()
            Topic.get(int(topic_id)).delete()
            Forum.filter(Forum.c.id==int(forum_id)).update(num_posts=Forum.c.num_posts-post_count, num_topics=Forum.c.num_topics-1)
            flash('删除成功！')
            return redirect(url_for(ForumView.forum_index, id=forum_id))
        else:
            flash('你无权限删除主题！')
            return redirect(url_for(ForumView.topic_view, forum_id=forum_id, topic_id=topic_id))
        
    @decorators.check_role('trusted')
    def post_actions(self):
        Post = get_model('forumpost')
        
        action = request.POST.get('action')
        post_id = request.POST.get('post_id')
        
        post = Post.get(int(post_id))
        if not post:
            return json({'msg':"没找到对应的发贴"})
        topic = post.topic
        flag = False
        topic_flag = False
        txt = ''
        msg = '处理成功'
        #topic
        is_manager = post.topic.forum.managers.has(request.user)
        if is_manager:
            if action == 'close':
                topic.closed = not topic.closed
                topic_flag = True
                txt = self.status['close'][topic.closed]
            elif action == 'top':
                topic.sticky = not topic.sticky
                topic_flag = True
                txt = self.status['sticky'][topic.sticky]
            elif action == 'essence':
                topic.essence = not topic.essence
                topic_flag = True
                txt = self.status['essence'][topic.essence]
            elif action == 'hidden':
                topic.hidden = not topic.hidden
                topic_flag = True
                txt = self.status['hidden'][topic.hidden]
            elif action == 'homepage':
                topic.homepage = not topic.homepage
                topic_flag = True
                txt = self.status['homepage'][topic.homepage]
            
        #post
        ok = False
        if is_manager or (post.posted_by.id == request.user.id and post.created_on+timedelta(days=settings.get_var('PARA/FORUM_EDIT_DELAY'))>=date.now()):
            if action == 'delete':
                if post.deleted:
                    #如果要反删除，如果是管理员则可以。如果不是，则如果是管理员
                    #删除的，则不能反删除
                    if is_manager:
                        ok = True
                    else:
                        if post.deleted_by.id == request.user.id:
                            ok = True
                        else:
                            msg = '此贴被管理员删除，你无法恢复'
                else:
                    ok = True
                if ok:
                    post.deleted = not post.deleted
                    if post.deleted:
                        post.deleted_by = request.user.id
                        post.deleted_on = date.now()
                    flag = True
                    txt = self.status['delete'][post.deleted]
            elif action == 'email':
                post.reply_email = not post.reply_email
                flag = True
                txt = self.status['email'][post.reply_email]
                #检查用户邮箱是否存在
                if post.reply_email and not post.posted_by.email:
                    msg = '您的邮箱尚未设置，将无法处理邮件'
                
        if flag:
            post.save()
        if topic_flag:
            topic.save()
        if flag or topic_flag:
            return json({'msg':msg, 'txt':txt})
        else:
            return json({'msg':'命令未识别或无权限, 未做修改'})
        
    def draw(self, forum_id, slug):
        import base64
        from StringIO import StringIO

        File = get_model('forumattachment')
        
        filename='forum/%s/%s.png' % (forum_id, slug)
        if request.method == 'POST':
            fobj = StringIO(base64.b64decode(request.params.get('text1')))
            nname=functions.save_file(filename, fobj)
            url_name=functions.get_href(nname)
            ff = File(slug=slug, file_name=nname, name=nname)
            ff.save()
            return {'url_name':url_name} 
        if request.method == 'GET':
            return {'forum_id':forum_id,'slug':slug}
    
    def id(self, pid):
        """
        根据pid跳转到相应的贴子
        """
        import math
        
        Post = get_model('forumpost')
        obj = Post.get_or_notfound(int(pid))
        while obj.parent:
            obj = obj.parent
        page = int(math.ceil(1.0*obj.floor/settings.get_var('PARA/FORUM_PAGE_NUMS')))
        url = '/forum/%d/%d?page=%d' % (obj.topic._forum_, obj._topic_, page)
        return redirect(url)