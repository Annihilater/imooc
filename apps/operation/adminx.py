#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/16 14:31
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : adminx.py
import xadmin
from apps.operation.models import (
    CourseComments,
    UserAsk,
    UserCourse,
    UserFavorite,
    UserMessage,
)
from libs.register_model import auto_register_all_model


# auto_register_all_model(__name__)
class CourseCommentsAdmin:
    list_display = ["id", "add_time", "user", "course", "usercourse_ptr", "comments"]
    list_filter = ["id", "add_time", "user", "course", "usercourse_ptr", "comments"]
    search_fields = ["id", "add_time", "user", "course", "usercourse_ptr", "comments"]


xadmin.site.register(CourseComments, CourseCommentsAdmin)


class UserAskAdmin:
    list_display = ["id", "add_time", "name", "mobile", "course_name"]
    list_filter = ["id", "add_time", "name", "mobile", "course_name"]
    search_fields = ["id", "add_time", "name", "mobile", "course_name"]


xadmin.site.register(UserAsk, UserAskAdmin)


class UserCourseAdmin:
    list_display = ["id", "add_time", "user", "course"]
    list_filter = ["id", "add_time", "user", "course"]
    search_fields = ["id", "add_time", "user", "course"]


xadmin.site.register(UserCourse, UserCourseAdmin)


class UserFavoriteAdmin:
    list_display = [
        "id",
        "add_time",
        "user",
        "fav_id",
        "fav_type",
    ]
    list_filter = [
        "id",
        "add_time",
        "user",
        "fav_id",
        "fav_type",
    ]
    search_fields = [
        "id",
        "add_time",
        "user",
        "fav_id",
        "fav_type",
    ]


xadmin.site.register(UserFavorite, UserFavoriteAdmin)


class UserMessageAdmin:
    list_display = ["id", "add_time", "user", "has_read", "message"]
    list_filter = ["id", "add_time", "user", "has_read", "message"]
    search_fields = ["id", "add_time", "user", "has_read", "message"]


xadmin.site.register(UserMessage, UserMessageAdmin)
