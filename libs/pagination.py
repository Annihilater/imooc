#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/20 17:43
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : pagination.py
from pure_pagination import Paginator, PageNotAnInteger


def django_pure_pagination(request, object_list, per_page):
    """
    使用 django-pure-pagination 插件进行分页
    :param request:request 对象
    :param object_list: 需要分页的对象
    :param per_page: 每页元素个数
    :return: 传给模板的分页对象
    """
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(object_list, per_page, request=request)
    return p.page(page)
