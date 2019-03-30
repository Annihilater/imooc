#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/22 14:21
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : url_help.py


def get_redirect_to(request):
    host = request.get_host()
    url_path = request.get_full_path().split('redirect_to=')[-1]
    redirect_to = request.scheme + '://' + host + url_path
    return redirect_to


def get_current_url(request):
    host = request.get_host()
    url_path = request.path
    redirect_to = request.scheme + '://' + host + url_path
    return redirect_to
