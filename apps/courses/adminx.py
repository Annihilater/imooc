#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/16 14:32
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : adminx.py
import xadmin
from apps.courses.models import Course, Lesson, Video, CourseResource


# from libs.register_model import auto_register_all_model


# auto_register_all_model(__name__)

class LessonInline:
    model = Lesson
    extra = 0


class CourseResourceInline:
    model = CourseResource
    extra = 0


class CourseAdmin:
    refresh_times = [3, 5, 7, 10]
    list_display = ["name", "degree", "learn_times", "students", "click_nums",
                    "fav_nums", "add_time", "get_chapter_num", "go_to"]
    list_filter = ["name", "degree", "learn_times", "students", "click_nums",
                   "fav_nums", "add_time"]
    search_fields = ["name", "degree", "learn_times", "students", "click_nums",
                     "fav_nums", "add_time"]
    model_icon = 'fa fa-table'  # 设置 icon
    ordering = ['-click_nums']  # 按字段排序
    readonly_fields = ['click_nums']  # 设置只读字段
    exclude = ['fav_nums']  # 隐藏字段
    style_fields = {'detail': 'ueditor'}
    import_excel = True

    inlines = [LessonInline, CourseResourceInline]

    # list_editable = ['degree']

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        """
        在保存课程的时候统计课程机构的课程数
        """
        new_course = self.new_obj
        new_course.save()
        if new_course.course_org:
            course_org = new_course.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            # 处理自己的逻辑
            pass
        return super(CourseAdmin, self).post(request, *args, **kwargs)


xadmin.site.register(Course, CourseAdmin)

from apps.courses.models import BannerCourse


class BannerCourseAdmin:
    list_display = ["name", "degree", "learn_times", "students", "click_nums",
                    "fav_nums", "add_time", "get_chapter_num", "go_to"]
    list_filter = ["name", "degree", "learn_times", "students", "click_nums",
                   "fav_nums", "add_time"]
    search_fields = ["name", "degree", "learn_times", "students", "click_nums",
                     "fav_nums", "add_time"]
    model_icon = 'fa fa-table'  # 设置 icon
    ordering = ['-click_nums']  # 按字段排序
    readonly_fields = ['click_nums']  # 设置只读字段
    exclude = ['fav_nums']  # 隐藏字段

    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


xadmin.site.register(BannerCourse, BannerCourseAdmin)


class LessonAdmin:
    list_display = ["name", "course", "click_nums", "fav_nums", "add_time"]
    list_filter = ["name", "course__name", "click_nums", "fav_nums", "add_time"]
    search_fields = ["name", "course", "click_nums", "fav_nums", "add_time"]


xadmin.site.register(Lesson, LessonAdmin)


class VideoAdmin:
    list_display = ["name", "lesson", "click_nums", "fav_nums", "add_time"]
    list_filter = ["name", "lesson", "click_nums", "fav_nums", "add_time"]
    search_fields = ["name", "lesson", "click_nums", "fav_nums", "add_time"]


xadmin.site.register(Video, VideoAdmin)


class CourseResourceAdmin:
    list_display = ["name", "course", "download", "click_nums", "fav_nums", "add_time"]
    list_filter = ["name", "course", "download", "click_nums", "fav_nums", "add_time"]
    search_fields = ["name", "course", "download", "click_nums", "fav_nums", "add_time"]


xadmin.site.register(CourseResource, CourseResourceAdmin)
