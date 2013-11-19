#! /usr/bin/env python
#coding=utf-8
from uliweb.orm import *
from uliweb.utils.common import get_var

def get_modified_user():
    from uliweb import request
    
    return request.user.id

class ForumCategory(Model):#板块
    name = Field(str, verbose_name='板块名称', max_length=100, required=True)
    description = Field(TEXT, verbose_name='板块描述')
    ordering = Field(int, verbose_name='排序',default = 1)
    created_on = Field(datetime.datetime, verbose_name='创建时间', auto_now_add=True)
    updated_on = Field(datetime.datetime, verbose_name='修改时间', auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return self.name
    
    class AddForm:
        fields = ['name', 'ordering']
        
    class EditForm:
        fields = ['name', 'ordering']

    class Table:
        fields = [
            {'name':'name', 'width':100},
            {'name':'ordering', 'width':40},
#            {'name':'action', 'verbose_name':'操作', 'width':100},
        ]

class Forum(Model):#论坛
    name = Field(str, verbose_name='论坛名称', max_length=100, required=True)
#    slug = models.SlugField(max_length = 110)#标签
    description = Field(TEXT, verbose_name='论坛描述')
    ordering = Field(int, verbose_name='排序',default = 1)
    category = Reference('forumcategory', verbose_name='所属板块', collection_name='forums', required=True)
    created_on = Field(datetime.datetime, verbose_name='创建时间', auto_now_add=True)
    updated_on = Field(datetime.datetime, verbose_name='修改时间', auto_now_add=True, auto_now=True)
    num_topics = Field(int, verbose_name='主题总数')
    num_posts = Field(int, verbose_name='文章总数')
#    attachments = Field(FILE, verbose_name='附件', hint='文件大小不能超过2M，请注意文件大小')

    last_reply_on = Field(datetime.datetime, verbose_name='最新回复时间', nullable=True)
    last_post_user = Reference('user', verbose_name='最后回复人', collection_name="last_post_user_forums", nullable=True)
    last_post = Field(int, verbose_name='最后发贴id', nullable=True)
    managers = ManyToMany('user', verbose_name='管理员')

    manager_only = Field(bool, verbose_name='是否只有管理员可以发贴')
    
    def __unicode__(self):
        return self.name
    
    class AddForm:
        fields = ['name', 'description', 'ordering', 'managers', 'manager_only']
        
    class EditForm:
        fields = ['name', 'description', 'ordering', 'managers', 'manager_only']
    
    class Table:
        fields = [
            {'name':'name', 'width':200},
            {'name':'description', 'width':200},
            {'name':'category', 'width':100},
            {'name':'ordering', 'width':40},
            {'name':'managers', 'width':100},
            {'name':'topictype'},
            {'name': 'manager_only', 'width': 100},
        ]
    
#class SubForum(Model):
#    forum = Reference('forum', verbose_name='所属论坛', collection_name='forum_subs', required=True)
#    name = Field(str, verbose_name="名称", max_length=100, required=True)
#    order = Field(int, verbose_name="顺序", default=999)
#    managers = ManyToMany('user', verbose_name='管理员')
    
class ForumTopicType(Model):
    forum = Reference('forum', verbose_name='所属论坛', collection_name='forum_topictypes', required=True)
    name = Field(str, verbose_name='主题分类名称', max_length=100, required=True)
#    slug = models.SlugField(max_length = 100)#标签
    description = Field(TEXT, verbose_name='主题分类描述')
    
    def __unicode__(self):
        return self.name
    
    class AddForm:
        fields = ['name']
        
    class EditForm:
        fields = ['name']
    
    class Table:
        fields = [
            {'name':'name', 'width':100},
        ]

class ForumTopic(Model):#主题
    forum = Reference('forum', verbose_name='所属主题', collection_name='forum_topics', required=True)
    topic_type = Reference('forumtopictype', verbose_name='主题类型', collection_name='topic_topictype')
    posted_by = Reference('user', verbose_name='发贴人', default=get_modified_user, auto_add=True, collection_name="user_topics")
    
    subject = Field(str, verbose_name='标题', max_length=999, required=True)
    num_views = Field(int, verbose_name='浏览次数',default = 1)
    num_replies = Field(int, verbose_name='回复总数',default = 1)#posts...
    created_on = Field(datetime.datetime, verbose_name='创建时间', auto_now_add=True)
    updated_on = Field(datetime.datetime, verbose_name='修改时间')
    last_reply_on = Field(datetime.datetime, verbose_name='最新回复时间')
    last_post_user = Reference('user', verbose_name='最后回复人', collection_name="last_post_user_topics")
    last_post = Field(int, verbose_name='最后发贴id')
    modified_user = Reference('user', verbose_name='最后修改人', default=get_modified_user, auto=True, collection_name="last_modified_user_topics")
    slug = Field(CHAR, max_length=32, verbose_name='唯一识别串')
    
    #Moderation features
    closed = Field(bool, verbose_name='是否关闭')
    sticky = Field(bool, verbose_name='是否置顶')
    hidden = Field(bool, verbose_name='是否隐藏')
    homepage = Field(bool, verbose_name='是否放首页')
    essence = Field(bool, verbose_name='是否精华贴')
    
    # 増加是否允许回复标志，缺省应为允许
    enable_comment = Field(bool, verbose_name='是否允许回复')

    class AddForm:
        fields = ['topic_type', 'subject', 'content',
                  'slug', 'reply_email', 'enable_comment']
        
    class EditForm:
        fields = ['topic_type', 'subject', 'content', 'slug']
        
    def __unicode__(self):
        return self.subject
    
class ForumAttachment(Model):
    slug = Field(CHAR, max_length=32, verbose_name='唯一识别串')
    file_name = Field(FILE, verbose_name='附件', hint='文件大小不能超过2M，请注意文件大小')
    name  = Field(str, verbose_name='文件显示名称', max_length=255)
    enabled = Field(bool, verbose_name='提交是否成功', default=False)
    created_on = Field(datetime.datetime, verbose_name='创建时间', auto_now_add=True)

# Create Replies for a topic
class ForumPost(Model):#can't edit...回复
    topic = Reference('forumtopic', verbose_name='所属主题', collection_name='topic_posts')
    posted_by = Reference('user', verbose_name='回复人', default=get_modified_user, auto_add=True, collection_name='user_posts')
    created_on = Field(datetime.datetime, verbose_name='创建时间', auto_now_add=True)
    content = Field(TEXT, verbose_name='文章信息', required=True)
    updated_on = Field(datetime.datetime, verbose_name='修改时间')
    floor = Field(int, verbose_name='楼层', required=True)
    deleted = Field(bool, verbose_name='删除标志', default=False)
    slug = Field(CHAR, max_length=32, verbose_name='唯一识别串')
    modified_by = Reference('user', verbose_name='修改人', collection_name='user_modified_posts')
    deleted_by = Reference('user', verbose_name='删除人', collection_name='user_deleted_posts')
    deleted_on = Field(datetime.datetime, verbose_name='删除时间')
    reply_email = Field(bool, verbose_name='有回复时是否邮件通知')
    parent = SelfReference(verbose_name='所属回复', collection_name='children_post')
    num_replies = Field(int, verbose_name='回复总数',default = 0)
    last_reply_on = Field(datetime.datetime, verbose_name='最新回复时间')
    last_post_user = Reference('user', verbose_name='最后回复人', collection_name='last_reply_user_post')

    @classmethod
    def OnInit(cls):
        Index('fpost_indx', cls.c.topic, cls.c.parent, cls.c.floor)
    
    class AddForm:
        fields = ['content', 'slug', 'reply_email']
    
class ForumMp3(Model):
        filename = Field(FILE, verbose_name='附件')
        datetime     = Field(datetime.datetime, auto_now_add=True)
 
