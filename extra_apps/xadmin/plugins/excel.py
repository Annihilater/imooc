#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/25 20:14
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : excel.py
from django.template import loader

import xadmin
from xadmin.views import ListAdminView, BaseAdminPlugin


class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html'))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)
