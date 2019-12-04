#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/17 07:13
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : forms.py
from captcha.fields import CaptchaField
from django import forms

from apps.users.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=32, min_length=3)
    password = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})
    redirect_to = forms.URLField(error_messages={'invalid': '跳转地址无效'})


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class RestPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True, min_length=8)
    password2 = forms.CharField(required=True, min_length=8)


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'nick_name', 'gender', 'birthday', 'address', 'mobile']


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=8)
    password2 = forms.CharField(required=True, min_length=8)
