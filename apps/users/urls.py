#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/18 19:02
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : urls.py
from django.urls import path

from apps.users.views import UserCenterView, UserCenterCourseVIew, UserCenterMessageVIew, UserCenterFavCourseVIew, \
    UserCenterFavOrgVIew, UserCenterFavTeacherVIew, ImageUploadView, UpdatePwdView, UpdateEmailView

urlpatterns = [
    path('', UserCenterView.as_view(), name='user_home'),
    path('course/', UserCenterCourseVIew.as_view(), name='user_course'),
    path('message/', UserCenterMessageVIew.as_view(), name='user_message'),
    path('fav/course/', UserCenterFavCourseVIew.as_view(), name='user_fav_course'),
    path('fav/teacher/', UserCenterFavTeacherVIew.as_view(), name='user_fav_teacher'),
    path('fav/org/', UserCenterFavOrgVIew.as_view(), name='user_fav_org'),

    # 用户头像上传
    path('image/upload/', ImageUploadView.as_view(), name='image_upload'),

    # 用户修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),

    # 修改邮箱
    path('email/update/', UpdateEmailView.as_view(), name='update_email'),
]
