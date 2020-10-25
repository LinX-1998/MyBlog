from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from mdeditor.fields import MDTextField


# 文章分类
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='博客分类')
    index = models.IntegerField(default=999, verbose_name='分类权重')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '博客分类'
        ordering = ['-index']

    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        queryset = Category.objects.all()
        return queryset


# 文章标签
class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='文章标签')
    index = models.IntegerField(default=999, verbose_name='分类权重')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '文章标签'
        ordering = ['-index']

    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        queryset = Tag.objects.all()
        return queryset


# 广告位
class Recommend(models.Model):
    name = models.CharField(max_length=1000, verbose_name='广告位')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '广告位'

    def __str__(self):
        return self.name


# 文章
class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    abstract = models.CharField(max_length=200, blank=True, verbose_name='摘要')
    # body = models.TextField(verbose_name="正文", help_text="正文必须为 MarkDown 格式")
    body = MDTextField(verbose_name="正文")
    is_life = models.BooleanField(default=False, verbose_name="生活笔记")
    is_technique = models.BooleanField(default=False, verbose_name="技术杂谈")
    can_comment = models.BooleanField(default=True, verbose_name="评论端口")
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    picture_type = models.PositiveIntegerField(default=0, verbose_name='图片值')
    img = models.ImageField(upload_to='article_img/%Y/%m/%d/', verbose_name='文章图片', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类', blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    recommend = models.ForeignKey(Recommend, on_delete=models.DO_NOTHING,
                                  verbose_name='博主推荐', blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_view():
        queryset = Article.objects.all().order_by('-views')[0:5]
        return queryset

    @staticmethod
    def get_by_recommend():
        queryset = Article.objects.filter(recommend=1).select_related()
        return queryset

    @staticmethod
    def get_by_category(category_name):
        category = Category.objects.get(name=category_name)
        queryset = Article.objects.filter(category=category)
        return queryset

    @staticmethod
    def get_by_tag(tag_name):
        tag = Tag.objects.get(name=tag_name)
        queryset = Article.objects.filter(tags=tag)
        return queryset

    @staticmethod
    def get_by_id(aid):
        queryset = Article.objects.get(id=aid)
        return queryset

    @staticmethod
    def get_by_detail(detail):
        if detail == '技术杂谈':
            queryset = Article.objects.filter(is_technique=True).select_related()
        elif detail == '生活笔记':
            queryset = Article.objects.filter(is_life=True).select_related()
        else:
            queryset = Article.objects.all().select_related()
        return queryset

    @staticmethod
    def get_by_title(search_title):
        queryset = Article.objects.filter(title__icontains=search_title).select_related()
        return queryset

    @staticmethod
    def get_all():
        queryset = Article.objects.all().select_related()
        return queryset

    @cached_property
    def new_tags(self):
        return ','.join(self.tags.values_list('name', flat=True))


# 轮播图
class Banner(models.Model):
    text_info = models.CharField(max_length=50, default='', verbose_name='标题')
    img = models.ImageField(upload_to='banner/', verbose_name='轮播图')
    link_url = models.URLField(max_length=100, verbose_name='图片链接')
    is_active = models.BooleanField(default=False, verbose_name='是否轮播')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.text_info

    class Meta:
        verbose_name = verbose_name_plural = '轮播图'
        ordering = ['id']

    @staticmethod
    def get_by_is_active():
        queryset = Banner.objects.filter(is_active=True)
        return queryset

    @staticmethod
    def get_by_not_active():
        queryset = Banner.objects.filter(is_active=False)
        return queryset


# 友情链接
class Link(models.Model):
    name = models.CharField(max_length=20, verbose_name='链接名称')
    index = models.IntegerField(default=999, verbose_name='友链权重')
    link_url = models.URLField(max_length=100, verbose_name='网址')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '友情链接'
        ordering = ['-index']

    @staticmethod
    def get_all():
        queryset = Link.objects.all()
        return queryset


# 评论表
class Comment(models.Model):
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    comment_body = models.CharField(max_length=2000, verbose_name='评论内容')
    user = models.CharField(max_length=100, verbose_name='评论者', blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='评论文章', blank=True, null=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='回复对象',
                                       blank=True, null=True, related_name='p_comment')

    class Meta:
        verbose_name = verbose_name_plural = '评论'

    def __str__(self):
        return self.comment_body

    @staticmethod
    def get_all():
        queryset = Comment.objects.all().select_related()
        return queryset

    @staticmethod
    def get_by_id(aid):
        article = Article.objects.get(id=aid)
        queryset = Comment.objects.filter(article=article)
        return queryset

    @staticmethod
    def get_by_cid(cid):
        queryset = Comment.objects.get(id=cid)
        return queryset


# 评论表
class Message(models.Model):
    message_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    message_body = models.CharField(max_length=2000, verbose_name='评论内容')
    user = models.CharField(max_length=100, verbose_name='评论者', blank=True, null=True)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='回复对象',
                                       blank=True, null=True, related_name='p_message')

    class Meta:
        verbose_name = verbose_name_plural = '信息'

    def __str__(self):
        return self.message_body

    @staticmethod
    def get_all():
        queryset = Message.objects.all().select_related().order_by('message_time')
        return queryset

    @staticmethod
    def get_by_mid(mid):
        queryset = Message.objects.get(id=mid)
        return queryset

    @staticmethod
    def get_count():
        count = Message.objects.all().count()
        return count
