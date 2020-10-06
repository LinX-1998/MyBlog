from django.contrib import admin
from django.urls import reverse
from blog.adminforms import ArticleAdminForm
from blog.models import Category, Tag, Article, Comment, Banner, Link, RecommendPosition, RecommendOut
from blog_config.base_admin import SuperBaseOwnerAdmin
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

admin.site.site_header = "翔仔的个人博客"
admin.site.site_title = "翔仔的博客管理后台"
admin.site.index_title = "首页"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'index', 'created_time', 'article_count']
    fields = ['name', 'index']

    def article_count(self, obj):
        return obj.article_set.count()
    article_count.short_description = "文章数量"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_time']
    fields = ['name']


@admin.register(Article)
class ArticleAdmin(SuperBaseOwnerAdmin):
    form = ArticleAdminForm
    list_display = ['title', 'user', 'category', 'views', 'created_time', 'modified_time', 'operator']
    fields = ['title', 'abstract', 'category', 'tags', 'img', 'body', 'views', 'recommend_position']
    list_display_links = []
    list_filter = ['category', ]
    search_fields = ['title', 'user__username']
    # filter_horizontal = ['tags', ]

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_article_change', args=(obj.id, ))
        )
    operator.short_description = "操作"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'comment_body', 'comment_time']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['text_info', 'link_url', 'is_active', 'created_time']
    fields = ['text_info', 'img', 'is_activate']


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'link_url', 'created_time']
    fields = ['name', 'link_url']


@admin.register(RecommendPosition)
class RecommendPositionAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_time']
    fields = ['name']


@admin.register(RecommendOut)
class RecommendOutAdmin(admin.ModelAdmin):
    list_display = ['title', 'introduction', 'link_url', 'created_time']
    fields = ['title', 'introduction', 'link_url']


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
