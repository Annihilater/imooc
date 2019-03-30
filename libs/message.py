#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/21 19:29
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : message.py
import json


def success(status='success', msg='成功'):
    res = dict(status=status, msg=msg)
    res = json.dumps(res)
    return res


def fail(status='fail', msg='失败'):
    res = dict(status=status, msg=msg)
    res = json.dumps(res)
    return res
