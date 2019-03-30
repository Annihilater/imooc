from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from apps.courses.models import Course
from apps.operation.models import UserFavorite
from apps.organization.models import CourseOrg, CityDict, Teacher
from libs.pagination import django_pure_pagination
from libs.search import search


class OrgView(View):
    """
    课程结构列表页
    """

    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        citys = CityDict.objects.all()

        all_orgs = search(request, all_orgs)

        orgs = all_orgs
        # 选取筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            city_id = int(city_id)
            orgs = all_orgs.filter(city_id=city_id)

        # 对机构类别进行筛选
        category = request.GET.get('ct', '')
        if category:
            orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')  # 排序
        if sort and sort == 'students':  # 按参与人数排序
            orgs = orgs.order_by('students')
        if sort and sort == 'courses':  # 按收藏人数排序
            orgs = orgs.order_by('course_nums')

        # 筛选全部完成之后在对总数进行统计
        org_nums = orgs.count()

        # 对课程机构进行分页
        orgs = django_pure_pagination(request, object_list=orgs, per_page=10)

        data = dict(orgs=orgs, pagination=orgs, citys=citys, org_nums=org_nums, query_city_id=city_id,
                    category=category, hot_orgs=hot_orgs, sort=sort)
        return render(request, 'org-list.html', data)


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True

        current_page = 'home'
        org = CourseOrg.objects.get(id=int(org_id))

        all_courses = org.course_set.all()
        all_teachers = org.teacher_set.all()
        data = dict(org=org, all_courses=all_courses, all_teachers=all_teachers, current_page=current_page,
                    has_fav=has_fav)
        return render(request, 'org-detail-homepage.html', data)


class OrgCourses(View):
    """
    机构课程页
    """

    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True

        current_page = 'course'
        org = CourseOrg.objects.get(id=int(org_id))
        all_courses = org.course_set.all()
        data = dict(org=org, all_courses=all_courses, current_page=current_page, has_fav=has_fav)
        return render(request, 'org-detail-course.html', data)


class OrgIntroduction(View):
    """
    机构介绍页
    """

    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True

        current_page = 'introduction'
        org = CourseOrg.objects.get(id=int(org_id))
        data = dict(org=org, current_page=current_page, has_fav=has_fav)
        return render(request, 'org-detail-desc.html', data)


class OrgTeachers(View):
    """
    机构讲师页
    """

    def get(self, request, org_id):
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True

        current_page = 'teacher'
        org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = org.teacher_set.all()
        data = dict(org=org, all_teachers=all_teachers, current_page=current_page, has_fav=has_fav)
        return render(request, 'org-detail-teachers.html', data)


class TeacherList(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        hot_teachers = teachers.order_by('-click_nums')[:5]

        teachers = search(request, teachers)

        # 对教师人气进行排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-click_nums')

        # 对教师列表进行分页
        teachers = django_pure_pagination(request, object_list=teachers, per_page=10)

        data = dict(teachers=teachers, pagination=teachers, sort=sort, hot_teachers=hot_teachers)
        return render(request, 'teachers-list.html', data)


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        hot_teachers = Teacher.hot_teachers()[:5]  # 讲师排行榜单

        teacher = Teacher.objects.get(id=int(teacher_id))
        courses = Course.objects.filter(teacher=teacher)

        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher_id, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True

        courses = django_pure_pagination(request, object_list=courses, per_page=2)
        data = dict(teacher=teacher, pagination=courses, courses=courses, hot_teachers=hot_teachers,
                    has_fav_teacher=has_fav_teacher, has_fav_org=has_fav_org)
        return render(request, 'teacher-detail.html', data)

# def get_sort_key(request, method, key):
#     new_key = ''
#     if method == 'get':
#         new_key = request.GET.get(key, '')
#     if method == 'post':
#         new_key = request.POST.get(key, '')
#     return new_key
#
#
# def sort(request, objects, sort, key):
#     sorted_objects = objects
#     if sort and sort == key:
#         sorted_objects = objects.order_by('-click_nums')
#     return sorted_objects
