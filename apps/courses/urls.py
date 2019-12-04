#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/18 19:02
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : urls.py
from django.urls import path

from apps.courses.views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentsView, AddCommentsView, \
    VideoView

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('info/<course_id>/', CourseInfoView.as_view(), name='course_info'),
    path('comments/<course_id>/', CourseCommentsView.as_view(), name='course_comments'),
    path('comments/add/', AddCommentsView.as_view(), name='add_comments'),
    path('video/<video_id>/', VideoView.as_view(), name='video'),

    # path('test/1', Test1.as_view(), name='test1'),
    # path('test/2', Test2.as_view(), name='test2'),
]
