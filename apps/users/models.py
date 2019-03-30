from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=(("male", "男"), ("female", "女")),
        default="male",
        verbose_name="性别",
    )
    address = models.CharField(max_length=100, default="", verbose_name="地址")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机")
    image = models.ImageField(
        upload_to="image/%Y/%m",
        default="image/default.png",
        max_length=100,
        verbose_name="头像",
        blank=True
    )
    email = models.EmailField(verbose_name='邮箱', null=True, blank=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def unread_msg_num(self):
        from apps.operation.models import UserMessage
        num = UserMessage.objects.filter(user=self.id, has_read=False).count()
        return num

    def clean_unread_message(self):
        """
        进入个人消息后清空未读消息
        """
        from apps.operation.models import UserMessage
        unread_messages = UserMessage.objects.filter(user=self.id, has_read=False)
        for message in unread_messages:
            message.has_read = True
            message.save()

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")
    send_type = models.CharField(
        max_length=20,
        choices=(("register", "注册"), ("forget", "找回密码"), ("update_email", "修改邮箱")),
        verbose_name="验证码类型",
    )
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    code = models.CharField(max_length=20, verbose_name="验证码")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def get_field(self):
        return ["id", "send_time", "send_type", "email", "code"]

    def __str__(self):
        return "{} {} {} {}".format(
            self.send_time, self.send_type, self.email, self.code
        )


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(
        upload_to="banner/%Y/%m", verbose_name="轮播图", max_length=100, blank=True
    )
    url = models.CharField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def get_field(self):
        return ["id", "title", "image", "url", "index", "add_time"]

    def __str__(self):
        return '{} {} {}'.format(self.title, self.index, self.add_time)
