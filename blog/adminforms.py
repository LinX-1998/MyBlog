# -*- coding: utf-8 -*-
"""
    @Author: LinXiang
    @Email: linxiang-1998@outlook.com
    @file: adminforms.py
    @time: 2020/10/6 13:32
    
    @introduce: Just a __init__.py file
"""
from django import forms


class ArticleAdminForm(forms.ModelForm):
    abstract = forms.CharField(widget=forms.Textarea, label="摘要", required=False)
