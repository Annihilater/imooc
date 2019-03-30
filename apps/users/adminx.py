#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/16 10:28
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : adminx.py

import xadmin
from apps.users.models import EmailVerifyRecord, Banner
from libs.register_model import auto_register_all_model

# auto_register_all_model(__name__)
from xadmin import views


class BaseSetting:
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting:
    site_title = '暮学后台管理系统'
    site_footer = '暮学在线网'
    menu_style = 'accordion'


xadmin.site.register(views.CommAdminView, GlobalSetting)


class EmailVerifyRecordAdmin(object):
    list_display = ["id", "send_time", "send_type", "email", "code"]
    list_filter = ["id", "send_time", "send_type", "email", "code"]
    search_fields = ["id", "send_time", "send_type", "email", "code"]


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class BannerAdmin:
    list_display = ["id", "title", "image", "url", "index", "add_time"]
    list_filter = ["id", "title", "image", "url", "index", "add_time"]
    search_fields = ["id", "title", "image", "url", "index", "add_time"]


xadmin.site.register(Banner, BannerAdmin)
