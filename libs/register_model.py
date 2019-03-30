#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/16 14:14
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : register_model.py
import inspect
import sys

import xadmin


def get_module_name(__name__):
    """
    获取应用下的 models 模块的字符串表现形式
    :param __name__: 调用该方法所在模块的 __name__ 属性
    :return: models 模块的字符串表现形式，例如：apps.users.models
    """
    module_name = __name__.split(".")[:-1]
    module_name.append("models")
    module_name = ".".join(module_name)
    return module_name


def get_obj_field(model):
    """
    获取模型下所有字段
    :param model: 模型
    :return: 字段列表
    """
    field_list = []
    for field in model.objects.model._meta.fields:  # field: users.Banner.id
        new_field = str(field).split(".")[-1]
        field_type = str(type(field)).split(".")[-1].replace("'>", "")
        field_list.append(new_field)
    print(model, field_list)
    return field_list


def register_single_model(model):
    """
    向 xadmin 注册单个模型
    :param model:模型
    """
    model_name = model._meta.object_name
    new_name = model_name + "Admin"
    data = dict(
        list_display=get_obj_field(model),
        list_filter=get_obj_field(model),
        search_fields=get_obj_field(model),
    )
    model_admin = type(new_name, (object,), data)
    xadmin.site.register(model, model_admin)


def auto_register_all_model(__name__):
    """
    自动注册 module 模块下除去 except_model 之外的所有 model
    :param module: 模块
    """
    module = get_module_name(__name__)
    model_module = sys.modules[module]
    obj_list = inspect.getmembers(model_module)
    for name, obj in obj_list:
        if not inspect.isclass(obj):  # 条件一：判断 obj 是否为类对象
            continue
        if name.startswith("__"):  # 条件二：判断 obj 是否为内置对象
            continue
        if obj.__class__.__name__ != "ModelBase":  # 条件三：判断 obj 是否为 ModelBase
            continue

        if (
            hasattr(obj, "_meta") and obj._meta.abstract is True
        ):  # 条件四：判断是否为抽象类，如果是抽象类就不需要注册
            continue

        xadmin_registry = xadmin.site.copy_registry()
        if obj in xadmin_registry["models"].keys():  # 判断模型是否已经注册
            continue

        register_single_model(obj)
