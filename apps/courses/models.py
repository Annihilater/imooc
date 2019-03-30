from datetime import datetime

import six
from DjangoUeditor.models import UEditorField
from django.db import models

# Create your models here.

from apps.organization.models import CourseOrg, Teacher


class Base(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")

    class Meta:
        abstract = True

    def get_field(self):
        return ["add_time", "click_nums", "fav_nums"]

    def __str__(self):
        return "{} {} {}".format(self.add_time, self.click_nums, self.fav_nums)


class Course(Base):
    name = models.CharField(max_length=50, verbose_name="课程名")
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', on_delete=models.DO_NOTHING, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=300, verbose_name="课程描述")
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    detail = UEditorField(u'内容	', width=600, height=300,
                          imagePath="courses/ueditor/image/%(basename)s_%(datetime)s.%",
                          filePath="courses/ueditor/file/%(basename)s_%(datetime)s.%",
                          upload_settings={"imageMaxSize": 1204000}, default='')
    degree = models.CharField(verbose_name="难度", max_length=20, choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")))
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    category = models.CharField(max_length=20, verbose_name='课程类别', default="后端开发")
    tag = models.CharField(max_length=150, verbose_name='课程标签', default='')
    image = models.ImageField(
        max_length=100, upload_to="courses/%Y/%m", verbose_name="封面图", blank=True
    )
    notice = models.CharField(max_length=1000, verbose_name="课程须知", null=True, blank=True)
    teacher_tell = models.CharField(max_length=1000, verbose_name="老师告诉你", null=True, blank=True)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_chapter_num(self):
        return self.lesson_set.all().count()

    get_chapter_num.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://www.baidu.com">跳转</a>')

    go_to.short_description = '跳转'

    def get_learn_students(self):
        students = self.usercourse_set.all().order_by('-add_time')
        if len(students) > 5:
            students = students[:5]
        return students

    def get_course_lesson(self):
        """
        获取课程所有章节
        """
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(Base):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100, verbose_name="章节名")
    url = models.CharField(max_length=300, default='', verbose_name='访问地址', null=True, blank=True)

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def get_field(self):
        return ["name", "course", "click_nums", "fav_nums", "add_time"]

    def __str__(self):
        return "{} {}".format(self.course, self.name)

    def get_lesson_video(self):
        """
        获得章节的所有视频
        """
        return self.video_set.all()


class Video(Base):
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100, verbose_name="视频名")
    video_time = models.IntegerField(default=0, verbose_name="视频时长")
    image = models.ImageField(
        max_length=100, upload_to="courses/video/%Y/%m", verbose_name="视频封面", blank=True, null=True
    )

    class Meta:
        verbose_name = "课程视频"
        verbose_name_plural = verbose_name

    def get_field(self):
        return ["name", "lesson", "click_nums", "fav_nums", "add_time"]

    def __str__(self):
        return self.name


class CourseResource(Base):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="资源文件")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def get_field(self):
        return ["name", "course", "download", "click_nums", "fav_nums", "add_time"]

    def __str__(self):
        return self.name
