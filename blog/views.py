import markdown
import json

from django.db import transaction
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import *
from django.contrib import messages
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.response import Response


def index(request):
    banners = Banner.get_by_is_active()
    hot_articles = Article.get_by_view()
    articles = Article.get_all()
    recommend_articles = Article.get_by_recommend()
    for i in articles:
        i.body = markdown.markdown(i.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    categories = Category.get_all()
    links = Link.get_all()
    tags = Tag.get_all()

    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger as e:
        contacts = paginator.page(1)
    except EmptyPage as e:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'email_url': settings.EMAIL_URL,
        'image_url': settings.IMAGE_URL,
        'banners': banners,
        'hot_articles': hot_articles,
        'articles': articles,
        'recommend_articles': recommend_articles,
        'categories': categories,
        'links': links,
        'tags': tags,
        'contacts': contacts,
    }
    return render(request, 'index.html', context=context)


def category_detail(request, category_name):
    articles = Article.get_by_category(category_name)
    recommend_articles = Article.get_by_recommend()
    for i in articles:
        i.body = markdown.markdown(i.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    categories = Category.get_all()
    links = Link.get_all()
    tags = Tag.get_all()

    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger as e:
        contacts = paginator.page(1)
    except EmptyPage as e:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'email_url': settings.EMAIL_URL,
        'contacts': contacts,
        'articles': articles,
        'categories': categories,
        'tags': tags,
        'links': links,
        'recommend_articles': recommend_articles,
    }

    return render(request, 'category.html', context=context)


def tag_detail(request, tag_name):
    articles = Article.get_by_tag(tag_name)
    recommend_articles = Article.get_by_recommend()
    for i in articles:
        i.body = markdown.markdown(i.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    categories = Category.get_all()
    links = Link.get_all()
    tags = Tag.get_all()

    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger as e:
        contacts = paginator.page(1)
    except EmptyPage as e:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'email_url': settings.EMAIL_URL,
        'contacts': contacts,
        'articles': articles,
        'categories': categories,
        'tags': tags,
        'links': links,
        'recommend_articles': recommend_articles,
    }

    return render(request, 'tag.html', context=context)


def blog_detail(request, detail):
    articles = Article.get_by_detail(detail)
    recommend_articles = Article.get_by_recommend()
    for i in articles:
        i.body = markdown.markdown(i.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    categories = Category.get_all()
    links = Link.get_all()
    tags = Tag.get_all()

    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger as e:
        contacts = paginator.page(1)
    except EmptyPage as e:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'email_url': settings.EMAIL_URL,
        'contacts': contacts,
        'articles': articles,
        'categories': categories,
        'tags': tags,
        'links': links,
        'recommend_articles': recommend_articles,
    }

    return render(request, 'nav.html', context=context)


def article_detail(request, aid):
    cid = request.GET.get('cid')
    comment = None
    if cid is None:
        cid = 0
    else:
        comment = Comment.get_by_cid(cid)
    article = Article.get_by_id(aid)
    comment_tree = create_comment_tree(article)
    recommend_articles = Article.get_by_recommend()
    article.views += 1
    article.save()
    article.body = markdown.markdown(article.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
    ])
    previous_article = Article.objects.filter(created_time__gt=article.created_time).last()
    next_article = Article.objects.filter(created_time__lt=article.created_time).first()

    categories = Category.get_all()
    links = Link.get_all()
    tags = Tag.get_all()

    context = {
        'email_url': settings.EMAIL_URL,
        'article': article,
        'comment_tree': comment_tree,
        'categories': categories,
        'tags': tags,
        'links': links,
        'recommend_articles': recommend_articles,
        'previous_article': previous_article,
        'next_article': next_article,
        'comment': comment,
        'cid': cid,
    }

    return render(request, 'article.html', context=context)


def search_detail(request):
    search_title = request.GET.get('search')
    articles = Article.get_by_title(search_title)
    recommend_articles = Article.get_by_recommend()
    for i in articles:
        i.body = markdown.markdown(i.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    categories = Category.get_all()
    links = Link.get_all()
    tags = Tag.get_all()

    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 10)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger as e:
        contacts = paginator.page(1)
    except EmptyPage as e:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'email_url': settings.EMAIL_URL,
        'contacts': contacts,
        'articles': articles,
        'categories': categories,
        'tags': tags,
        'links': links,
        'recommend_articles': recommend_articles,
    }

    return render(request, 'search.html', context=context)


def find_parent_comment(comment_tree, comment):
    for parent, value in comment_tree.items():
        if parent == comment.parent_comment:
            comment_tree[parent][comment] = {}
        else:
            find_parent_comment(comment_tree[parent], comment)


def create_comment_tree(article):
    all_comments = article.comment_set.select_related().order_by('comment_time')
    comment_tree = {}

    for comment in all_comments:
        if comment.parent_comment is None:
            comment_tree[comment] = {}
        else:
            find_parent_comment(comment_tree, comment)

    return comment_tree


def comment_detail(request, aid):
    user = request.POST.get('your_name')
    comment_body = request.POST.get('your_body')
    article = Article.get_by_id(aid)
    cid = request.POST.get('her_name')
    print("YES", article.id)
    print(cid)
    print("YES")
    with transaction.atomic():
        if cid == 0:
            comment_obj = Comment.objects.create(user=user, comment_body=comment_body, article=article)
        else:
            comment = Comment.get_by_cid(cid)
            comment_obj = Comment.objects.create(user=user, comment_body=comment_body, article=article, parent_comment=comment)
    messages.add_message(request, messages.SUCCESS, '评论发表成功', extra_tags='success')
    return redirect(to=article_detail, aid=aid)

