from datetime import datetime

from django.db import models


# Create your models here.


class Base(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")

    class Meta:
        abstract = True


class CityDict(Base):
    name = models.CharField(max_length=20, verbose_name="城市")
    description = models.CharField(max_length=200, verbose_name="城市描述")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def get_field(self):
        return ["id", "add_time", "click_nums", "fav_nums", "name", "description"]

    def __str__(self):
        return self.name


class CourseOrg(Base):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    category = models.CharField(max_length=20, verbose_name='机构类别',
                                choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')))
    description = models.TextField(verbose_name="机构描述")
    type = models.CharField(max_length=10, verbose_name="机构标签", default="全国知名")
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数')
    image = models.ImageField(max_length=100, upload_to="org/%Y/%m", verbose_name="封面图", blank=True)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    city = models.ForeignKey(CityDict, verbose_name="所在城市", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    def get_teacher_num(self):
        """
        获取课程机构的教师数量
        """
        teacher_num = self.teacher_set.all().count()
        return teacher_num

    def get_field(self):
        return [
            "id",
            "add_time",
            "click_nums",
            "fav_nums",
            "name",
            "description",
            "image",
            "address",
            "city",
        ]

    def __str__(self):
        return self.name


class Teacher(Base):
    org = models.ForeignKey(CourseOrg, verbose_name="所属机构", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50, verbose_name="教师名称")
    age = models.IntegerField(default=30, verbose_name="年龄")
    course_nums = models.IntegerField(default=0, verbose_name='课程数', null=True, blank=True)
    image = models.ImageField(max_length=100, upload_to="teacher/%Y/%m", verbose_name="头像", null=True, blank=True)
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")

    class Meta:
        verbose_name = "讲师"
        verbose_name_plural = verbose_name

    @classmethod
    def hot_teachers(cls):
        hot_teachers = Teacher.objects.all().order_by('-click_nums')
        return hot_teachers

    @property
    def student_num(self):
        from apps.courses.models import Course
        courses = Course.objects.filter(teacher=self)
        student_num = 0
        for course in courses:
            student_num += course.students
        return student_num

    def course_num(self):
        return self.course_set.all().count()

    def get_field(self):
        return [
            "id",
            "add_time",
            "click_nums",
            "fav_nums",
            "org",
            "name",
            "work_years",
            "work_company",
            "work_position",
            "points",
        ]

    def __str__(self):
        return self.name
