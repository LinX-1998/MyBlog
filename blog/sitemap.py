# -*- coding: utf-8 -*-
"""
    @Author: LinXiang
    @Email: linxiang-1998@outlook.com
    @file: sitemap.py
    @time: 2020/10/17 18:03
    
    @introduce: Just a __init__.py file
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6
    protocol = 'https'

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return reverse('article_detail', args=[obj.id])
