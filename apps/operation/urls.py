#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/18 18:56
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : urls.py
from django.urls import path

from apps.operation.views import AddUserAskView

urlpatterns = [
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
]
