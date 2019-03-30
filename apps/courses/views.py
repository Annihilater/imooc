import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from apps.courses.models import Course, CourseResource, Video
from apps.operation.models import UserFavorite, CourseComments, UserCourse

from libs.login import LoginRequiredMixin
from libs.pagination import django_pure_pagination
from libs.search import search


# also_learning_courses = Course.objects.filter(usercourse__user_id__in=user_id_list).order_by('-click_nums')[:5]
def also_learning_course(course):
    user_courses = UserCourse.objects.filter(course=course)  # 得到学习该课程的用户课程表
    user_id_list = [user_course.user_id for user_course in user_courses]  # 得到学习该课程的所有用户的 id
    course_id_list = UserCourse.objects.filter(user_id__in=user_id_list)
    also_learning_courses = Course.objects.filter(id__in=course_id_list)
    return also_learning_courses


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all()
        hot_courses = all_courses.order_by('-click_nums')

        all_courses = search(request, all_courses)

        recommend_courses = hot_courses[:3]
        courses = all_courses.order_by('-add_time')

        sort = request.GET.get('sort', '')  # 排序
        if sort and sort == 'hot':  # 按照点击数排序
            courses = hot_courses
        if sort and sort == 'students':  # 安装参与人数排序
            courses = courses.order_by('-students')

        # 对课程进行分页
        courses = django_pure_pagination(request, object_list=courses, per_page=10)

        data = dict(courses=courses, pagination=courses, hot_courses=hot_courses, recommend_courses=recommend_courses,
                    sort=sort)
        return render(request, 'course-list.html', data)


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 增加各种点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False
        has_study = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
            if UserCourse.objects.filter(user=request.user, course=course):
                has_study = True

        relate_courses = []
        if course.tag:
            relate_courses = Course.objects.filter(tag=course.tag).order_by('-click_nums')[:3]

        data = dict(course=course, relate_courses=relate_courses, has_fav_org=has_fav_org,
                    has_fav_course=has_fav_course, has_study=has_study)
        return render(request, 'course-detail.html', data)


class CourseInfoView(LoginRequiredMixin, View):

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()

        #  查询用户有没有学习课程，如果没有没有学习，那么就表示用户现在开始学习课程，将用户和课程的关联关系数据保存到数据库
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        course_resources = CourseResource.objects.filter(course=course)

        also_learning_courses = also_learning_course(course)
        data = dict(course=course, course_resources=course_resources, also_learning_courses=also_learning_courses)
        return render(request, 'course-info.html', data)


class CourseCommentsView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course_resources = CourseResource.objects.filter(course=course)
        course_comments = CourseComments.objects.filter(course=course)
        also_learning_courses = also_learning_course(course)
        data = dict(course=course, course_resources=course_resources, course_comments=course_comments,
                    also_learning_courses=also_learning_courses)
        return render(request, 'course-comment.html', data)


class AddCommentsView(LoginRequiredMixin, View):
    """
    发表评论
    """

    def post(self, request):
        if not request.user.is_authenticated:
            status = 'fail'
            msg = '用户未登录'
            return HttpResponse(json.dumps(dict(status=status, msg=msg)), content_type='application/json')

        course_id = request.POST.get('course_id', '')
        comments = request.POST.get('comments', '')
        status = 'fail'
        msg = '添加失败'

        if course_id and comments:
            course = Course.objects.get(id=int(course_id))
            course_comments = CourseComments()
            course_comments.course = course
            course_comments.user = request.user
            course_comments.comments = comments
            course_comments.save()
            status = 'success'
            msg = '添加成功'

        return HttpResponse(json.dumps(dict(status=status, msg=msg)), content_type='application/json')


class VideoView(View):
    """
    视频播放页面
    """

    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        course = video.lesson.course

        #  查询用户有没有学习课程，如果没有没有学习，那么就表示用户现在开始学习课程，将用户和课程的关联关系数据保存到数据库
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        course_resources = CourseResource.objects.filter(course=course)

        also_learning_courses = also_learning_course(course)
        data = dict(course=course, course_resources=course_resources, also_learning_courses=also_learning_courses,
                    video=video)
        return render(request, 'course-video.html', data)

# class Test1(View):
#     def get(self, request):
#         return render(request, 'test1.html')
#
#
# class Test2(View):
#     def get(self, request):
#         return render(request, 'test2.html')
