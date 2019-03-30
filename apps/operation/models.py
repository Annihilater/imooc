from datetime import datetime

from django.db import models

# Create your models here.
from apps.courses.models import Course
from apps.users.models import UserProfile


class Base(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        abstract = True


class UserCourse(Base):
    user = models.ForeignKey(
        UserProfile, verbose_name="用户", on_delete=models.DO_NOTHING
    )
    course = models.ForeignKey(Course, verbose_name="课程",
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} {}'.format(self.user, self.course)


class UserAsk(Base):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=50, verbose_name="课程名")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def get_field(self):
        return ["id", "add_time", "name", "mobile", "course_name"]

    def __str__(self):
        return self.name, self.mobile, self.course_name


class CourseComments(UserCourse):
    comments = models.CharField(max_length=200, verbose_name="评论")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def get_field(self):
        return ["id", "add_time", "user", "course", "usercourse_ptr", "comments"]

    def __str__(self):
        return '{} {} {}'.format(self.user, self.course, self.comments)


class UserFavorite(Base):
    user = models.ForeignKey(
        UserProfile, verbose_name="用户", on_delete=models.DO_NOTHING
    )
    fav_id = models.IntegerField(default=0, verbose_name="数据id")
    fav_type = models.IntegerField(
        default=1, choices=((1, "课程"), (2, "课程机构"), (3, "讲师")), verbose_name="收藏类型"
    )

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} {} {}'.format(self.user, self.fav_type, self.fav_id)


class UserMessage(Base):
    user_group = models.IntegerField(verbose_name='接收信息的用户组', default=3,
                                     choices=((1, "所有用户"), (2, "所有管理员"), (3, "单个用户")), )
    user = models.IntegerField(default=0, verbose_name="接收用户的 id")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    message = models.CharField(max_length=500, verbose_name="消息内容")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{} {} {}'.format(self.user, self.has_read, self.message)


