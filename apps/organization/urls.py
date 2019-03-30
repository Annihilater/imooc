#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/18 18:58
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : urls.py
from django.urls import path

from apps.operation.views import AddFavView
from apps.organization.views import OrgView, OrgHomeView, OrgCourses, OrgIntroduction, OrgTeachers

urlpatterns = [
    # 课程机构首页
    path('', OrgView.as_view(), name='org_list'),
    path('home/<org_id>/', OrgHomeView.as_view(), name='org_home'),
    path('courses/<org_id>/', OrgCourses.as_view(), name='org_courses'),
    path('introduction/<org_id>/', OrgIntroduction.as_view(), name='org_introduction'),
    path('teachers/<org_id>/', OrgTeachers.as_view(), name='org_teachers'),

    # 机构收藏功能
    path('add_fav/', AddFavView.as_view(), name='add_fav'),
]
