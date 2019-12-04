#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/17 15:40
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : email_send.py
from random import Random

from django.core.mail import send_mail

from apps.users.models import EmailVerifyRecord
from imooc.settings import EMAIL_FROM


def gen_random_str(random_length=8):
    r = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    length = len(chars)
    random = Random()
    for i in range(random_length):
        r += chars[random.randint(0, length - 1)]
    return r


def gen_email_code(random_length=6):
    r = ''
    chars = '1234567890'
    length = len(chars)
    random = Random()
    for i in range(random_length):
        r += chars[random.randint(0, length - 1)]
    return r


def send_email(email, send_type='register'):
    """
    :param email:接收的邮件的邮箱
    :param send_type: 邮件发送类型
    """
    # 修改邮箱的验证码长度为6位数字，注册和重置密码的验证码长度为16位数字大小写字母组合
    if send_type == 'update_email':
        code = gen_email_code()
    else:
        code = gen_random_str()

    email_record = EmailVerifyRecord()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '慕学在线网注册激活链接'
        email_body = '请点击下面链接激活你的账户: http://127.0.0.1:8000/active/{0}'.format(email_record.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print('email has been send')

    if send_type == 'forget':
        email_title = '慕学在线网密码重置链接'
        email_body = '请点击下面链接重置您的密码: http://127.0.0.1:8000/reset/{0}'.format(email_record.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print('email has been send')

    if send_type == 'update_email':
        email_title = '慕学在线网邮箱修改验证码'
        email_body = '您的邮箱验证码为: {0}'.format(email_record.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print('email has been send')
