#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/16 14:23
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : adminx.py
import xadmin
from apps.organization.models import CityDict, CourseOrg, Teacher
from libs.register_model import auto_register_all_model


# auto_register_all_model(__name__)
class CityDictAdmin:
    list_display = ["id", "add_time", "click_nums", "fav_nums", "name", "description"]
    list_filter = ["id", "add_time", "click_nums", "fav_nums", "name", "description"]
    search_fields = ["id", "add_time", "click_nums", "fav_nums", "name", "description"]


xadmin.site.register(CityDict, CityDictAdmin)


class CourseOrgAdmin:
    list_display = ["id", "add_time", "click_nums", "fav_nums", "name", "address", "city"]
    list_filter = ["id", "add_time", "click_nums", "fav_nums", "name", "address", "city"]
    search_fields = ["id", "add_time", "click_nums", "fav_nums", "name", "address", "city"]
    relfield_style = ['fk-ajax']


xadmin.site.register(CourseOrg, CourseOrgAdmin)


class TeacherAdmin:
    list_display = [
        "id",
        "add_time",
        "click_nums",
        "fav_nums",
        "org",
        "name",
        "work_years",
        "work_company",
        "work_position",
        "points",
    ]
    list_filter = [
        "id",
        "add_time",
        "click_nums",
        "fav_nums",
        "org",
        "name",
        "work_years",
        "work_company",
        "work_position",
        "points",
    ]
    search_fields = [
        "id",
        "add_time",
        "click_nums",
        "fav_nums",
        "org",
        "name",
        "work_years",
        "work_company",
        "work_position",
        "points",
    ]


xadmin.site.register(Teacher, TeacherAdmin)
