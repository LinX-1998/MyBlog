from django.db import models
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField


# 文章分类
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='博客分类')
    index = models.IntegerField(default=999, verbose_name='分类排序')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '博客分类'

    def __str__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='文章标签')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '文章标签'

    def __str__(self):
        return self.name


# 广告位
class RecommendPosition(models.Model):
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
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    img = models.ImageField(upload_to='article_img/%Y/%m/%d/', verbose_name='文章图片', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='分类', blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    recommend_position = models.ForeignKey(RecommendPosition, on_delete=models.DO_NOTHING,
                                           verbose_name='博主推荐', blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = '文章'

    def __str__(self):
        return self.title


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


# 友情链接
class Link(models.Model):
    name = models.CharField(max_length=20, verbose_name='链接名称')
    link_url = models.URLField(max_length=100, verbose_name='网址')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '友情链接'


# 评论表
class Comment(models.Model):
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    comment_body = models.CharField(max_length=2000, verbose_name='评论内容')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者', blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='文章', blank=True, null=True)

    class Meta:
        verbose_name = verbose_name_plural = '评论'

    def __str__(self):
        return self.comment_body


# 推荐文章
class RecommendOut(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    introduction = models.CharField(max_length=3000, verbose_name='说明')
    link_url = models.CharField(max_length=100, verbose_name='网址')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.link_url

    class Meta:
        verbose_name = verbose_name_plural = '推荐文章'