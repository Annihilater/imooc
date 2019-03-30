#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/21 00:36
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : search.py
from django.db.models import Q


def search(request, objects):
    # 全局搜索
    results = objects
    type = request.GET.get('type', '')
    keywords = request.GET.get('keywords', '')

    if type == 'course' and keywords:  # 课程搜索
        results = objects.filter(Q(name__icontains=keywords) | Q(detail__icontains=keywords))

    if type == 'teacher' and keywords:  # 讲师搜索
        results = objects.filter(Q(name__icontains=keywords))

    if type == 'org' and keywords:  # 机构搜索
        results = objects.filter(Q(name__icontains=keywords) | Q(description__icontains=keywords))

    return results
