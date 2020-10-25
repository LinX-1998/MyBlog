"""blog_config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from blog.views import *
from django.contrib.sitemaps import views as sitemap_views
from blog.sitemap import ArticleSitemap

urlpatterns = [
    path(r'admin/', admin.site.urls, name='admin'),
    path(r'', index, name='index'),
    path(r'category/<str:category_name>.html', category_detail, name='category_detail'),
    path(r'tag/<str:tag_name>.html', tag_detail, name='tag_detail'),
    path(r'blog/<str:detail>.html', blog_detail, name='blog_detail'),
    path(r'article/<int:aid>.html', article_detail, name='article_detail'),
    path(r'search/', search_detail, name='search_detail'),
    path(r'comment/<int:aid>', comment_detail, name='comment_detail'),
    path(r'mdeditor/', include('mdeditor.urls')),
path('sitemap.xml', sitemap_views.sitemap, {'sitemaps': {'articles': ArticleSitemap}}, name='django.contrib.sitemaps.views.sitemap'),
]

