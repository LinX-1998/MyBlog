# -*- coding: utf-8 -*-
"""
    @Author: LinXiang
    @Email: linxiang-1998@outlook.com
    @file: custom.py
    @time: 2020/10/15 1:28
    
    @introduce: Just a __init__.py file
"""
from django import template
from django.utils.safestring import mark_safe
register = template.Library()


def research_build_tree(html, tree, indent):
    for key, value in tree.items():
        row = '''<div class="margin-up-10" style="background-color:#fbfdfb; border:1px solid #eee; margin-left:%spx;">
                    <div class='margin-left-10 margin-up-2'>%s</div>
                    <div class='margin-left-10 margin-up-2'>
                        <span class='font-color-min-green'>%s</span>
                        <span class='margin-left-5'>%s</span>
                        <a href='/article/%s.html?cid=%s#comment_position'>
                        <span class='margin-left-5 font-color-min-green'>回复</span>
                        </a>
                    </div>
                    </div>
                    ''' % (indent, key.comment_body, key.user, key.comment_time.strftime('%Y-%m-%d %T'), key.article.id, key.id)

        html += row
        if value:
            html = research_build_tree(html, tree[key], indent+50)
    return html


@register.simple_tag
def build_comment_tree(comment_tree):

    html = "<div style='border: 1px solid white;'>"

    for key, value in comment_tree.items():
        row = '''<div class="margin-left-20 margin-up-10" style="background-color:#fbfdfb; border:1px solid #eee;">
            <div class='margin-left-10 margin-up-2'>%s</div>
            <div class='margin-left-10 margin-up-2'>
                <span class='font-color-min-green'>%s</span>
                <span class='margin-left-5'>%s</span>
                <a href='/article/%s.html?cid=%s#comment_position'>
                <span class='margin-left-5 font-color-min-green'>回复</span>
                </a>
            </div>
            </div>''' % (key.comment_body, key.user, key.comment_time.strftime('%Y-%m-%d %T'), key.article.id, key.id)
        html += row

        if value:
            html = research_build_tree(html, comment_tree[key], 70)
    html += "<div class='height-10'></div></div>"
    return mark_safe(html)
