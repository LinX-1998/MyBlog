# -*- coding: utf-8 -*-
"""
    @Author: LinXiang
    @Email: linxiang-1998@outlook.com
    @file: base_admin.py
    @time: 2020/10/6 14:36
    
    @introduce: Just a __init__.py file
"""
from django.contrib import admin


class SuperBaseOwnerAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(SuperBaseOwnerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super(SuperBaseOwnerAdmin, self).save_model(request, obj, form, change)
