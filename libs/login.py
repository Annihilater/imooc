#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/20 11:14
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : login.py
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin as _LoginRequiredMixin
from django.views.generic.base import View


class LoginRequiredMixin(_LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class LoginRequiredMixinView(_LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

# class LoginRequiredMixin:
#
#     @method_decorator(login_required(login_url='/login/'))
#     def dispatch(self, request, *args, **kwargs):
#         return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
