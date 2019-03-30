#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/23 11:49
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : fav_help.py
from apps.courses.models import Course
from apps.organization.models import CourseOrg, Teacher


def reduce_fav_num(fav_type, fav_id):
    """
    :param fav_type:int 类型，收藏类型
    :param fav_id: int 类型， 收藏 id
    """
    if fav_type == 1:
        course = Course.objects.get(id=fav_id)
        if course.fav_nums < 1:
            course.fav_nums = 0
        else:
            course.fav_nums -= 1
        course.save()
    if fav_type == 2:
        org = CourseOrg.objects.get(id=fav_id)
        if org.fav_nums < 1:
            org.fav_nums = 0
        else:
            org.fav_nums -= 1
        org.save()
    if fav_type == 3:
        teacher = Teacher.objects.get(id=fav_id)
        if teacher.fav_nums < 1:
            teacher.fav_nums = 0
        else:
            teacher.fav_nums -= 1
        teacher.save()


def add_fav_num(fav_type, fav_id):
    """
    :param fav_type:int 类型，收藏类型
    :param fav_id: int 类型， 收藏 id
    """
    if fav_type == 1:
        course = Course.objects.get(id=fav_id)
        course.fav_nums += 1
        course.save()
    if fav_type == 2:
        org = CourseOrg.objects.get(id=fav_id)
        org.fav_nums += 1
        org.save()
    if fav_type == 3:
        teacher = Teacher.objects.get(id=fav_id)
        teacher.fav_nums += 1
        teacher.save()
