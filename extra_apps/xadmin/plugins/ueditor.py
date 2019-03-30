#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/25 18:32
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : ueditor.py
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from django.conf import settings

import xadmin
from xadmin.views import BaseAdminPlugin, CreateAdminView, UpdateAdminView


class XadminUEditorWidget(UEditorWidget):
    def __init__(self, **kwargs):
        self.ueditor_options = kwargs
        self.Media.js = None
        super(XadminUEditorWidget, self).__init__(kwargs)


class UeditorPlugin(BaseAdminPlugin):
    def get_filed_style(self, attrs, db_field, style, **kwargs):
        if style == 'ueditor' and isinstance(db_field, UEditorField):
            widget = db_field.formfield().widget
            param = {}
            param.update(widget.ueditor_settings)
            param.update(widget.attrs)
            return dict(widget=XadminUEditorWidget(**param))
        return attrs

    def block_extrahead(self, context, nodes):
        js = '<script type="text/javascript" src="{}"></script>'.format(
            settings.STATIC_URL + 'ueditor/ueditor.config.js')
        js += '<script type="text/javascript" src="{}"></script>'.format(
            settings.STATIC_URL + 'ueditor/ueditor.all.min.js')
        nodes.append(js)


xadmin.site.register_plugin(UeditorPlugin, CreateAdminView)
xadmin.site.register_plugin(UeditorPlugin, UpdateAdminView)