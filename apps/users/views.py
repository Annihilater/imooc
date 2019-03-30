import json

from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

from apps.courses.models import Course
from apps.operation.models import UserMessage, UserFavorite, UserCourse
from apps.organization.models import Teacher, CourseOrg
from apps.users.forms import LoginForm, RegisterForm, ForgetPwdForm, RestPwdForm, ImageUploadForm, ModifyPwdForm, \
    UserInfoForm
from apps.users.models import UserProfile, EmailVerifyRecord, Banner
from libs.email_send import send_email
from libs.message import success, fail
from libs.login import LoginRequiredMixinView
from libs.pagination import django_pure_pagination
from libs.url_help import get_redirect_to, get_current_url


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = authenticate(username=username, password=password)
#         if user:
#             auth_login(request, user)
#             return render(request, 'index.html', {})
#         return render(request, 'login.html', {'msg': '用户名或密码错误'})
#
#     if request.method == 'GET':
#         return render(request, 'login.html', {})

class IndexView(View):
    def get(self, request):
        banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        orgs = CourseOrg.objects.all()[:15]
        data = dict(banners=banners, courses=courses, banner_courses=banner_courses, orgs=orgs)
        return render(request, 'index.html', data)


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        login_form = LoginForm()
        if register_form.is_valid():
            email = register_form.data.get('email', '')
            password = register_form.data.get('password', '')
            if UserProfile.objects.filter(email=email):
                msg = '用户已存在请直接登录'
                data = dict(msg=msg, login_form=login_form)
                return render(request, 'login.html', data)
            user = UserProfile()
            user.email = email
            user.password = make_password(password)
            user.is_active = False
            user.save()

            # 注册成功后发送一条欢迎消息
            user_message = UserMessage(user=user, message='欢迎注册慕学在线网')
            user_message.save()

            send_email([email], send_type='register')
            return redirect('login')
        return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        redirect_to = get_redirect_to(request)  # 获取完整的重定向地址
        data = dict(login_form=login_form, redirect_to=redirect_to)
        return render(request, 'login.html', data)

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            login_url = get_current_url(request)
            username = login_form.cleaned_data.get('username', '')
            password = login_form.cleaned_data.get('password', '')
            redirect_to = login_form.cleaned_data.get('redirect_to', '')
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                auth_login(request, user)
                if redirect_to and redirect_to != login_url:
                    return redirect(redirect_to)
                return redirect('index')
            login_form = LoginForm()
            return render(request, 'login.html', {'msg': '用户名或密码错误或账户未激活', 'login_form': login_form})
        return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('index')


class ActiveView(View):
    def get(self, request, activate_code):
        email_verify_record = EmailVerifyRecord.objects.filter(code=activate_code)
        if email_verify_record:
            email = eval(email_verify_record[0].email)[0]
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
            login_form = LoginForm()
            data = dict(login_form=login_form)
            return render(request, 'login.html', data)
        return render(request, 'active_fail.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_pwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form})

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = forget_pwd_form.data.get('email', '')
            if UserProfile.objects.filter(email=email):
                send_email([email], send_type='forget')
                return render(request, 'send_success.html')

        return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form})


class RestPwdView(View):
    def get(self, request, reset_code):
        reset_pwd_form = RestPwdForm()
        email_verify_record = EmailVerifyRecord.objects.filter(code=reset_code)
        if email_verify_record:
            email = eval(email_verify_record[0].email)[0]
            return render(request, 'password_reset.html', {'reset_pwd_form': reset_pwd_form, 'email': email})


class ModifyPwdView(View):
    """
    修改用户密码
    """

    def post(self, request):
        reset_pwd_form = RestPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            email = reset_pwd_form.data.get('email', '')
            password1 = reset_pwd_form.data.get('password1', '')
            password2 = reset_pwd_form.data.get('password2', '')

            if password1 == password2:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(password1)
                user.save()
                return render(request, 'login.html')
        return render(request, 'password_reset.html', {'reset_pwd_form': reset_pwd_form})


class UserCenterView(LoginRequiredMixinView):
    def get(self, request, ):
        user = request.user
        data = dict(user=user)
        return render(request, 'usercenter-info.html', data)

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, request.FILES, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse(dict(status='success'))
        return JsonResponse(user_info_form.errors)


class UserCenterCourseVIew(LoginRequiredMixinView):
    def get(self, request):
        user = request.user
        user_course_list = UserCourse.objects.filter(user=user)
        course_id_list = [user_course.course_id for user_course in user_course_list]
        courses = [Course.objects.get(id=course_id) for course_id in course_id_list]
        courses = django_pure_pagination(request, courses, per_page=8)
        data = dict(courses=courses, pagination=courses)
        return render(request, 'usercenter-mycourse.html', data)


class UserCenterMessageVIew(LoginRequiredMixinView):
    def get(self, request):
        user_id = int(request.user.id)
        user_messages = UserMessage.objects.filter(user=user_id)
        request.user.clean_unread_message()  # 清空未读消息

        messages = django_pure_pagination(request, user_messages, per_page=7)
        data = dict(messages=messages, pagination=messages)
        return render(request, 'usercenter-message.html', data)


class UserCenterFavCourseVIew(LoginRequiredMixinView):
    def get(self, request):
        user = request.user
        user_favorite_list = UserFavorite.objects.filter(user=user, fav_type=1)
        course_id_list = [user_favorite.fav_id for user_favorite in user_favorite_list]
        courses = [Course.objects.get(id=course_id) for course_id in course_id_list]
        courses = django_pure_pagination(request, courses, per_page=8)
        data = dict(courses=courses, pagination=courses)
        return render(request, 'usercenter-fav-course.html', data)


class UserCenterFavOrgVIew(LoginRequiredMixinView):
    def get(self, request):
        user = request.user
        user_favorite_list = UserFavorite.objects.filter(user=user, fav_type=2)
        org_id_list = [user_favorite.fav_id for user_favorite in user_favorite_list]
        orgs = [CourseOrg.objects.get(id=org_id) for org_id in org_id_list]
        orgs = django_pure_pagination(request, orgs, per_page=5)
        data = dict(orgs=orgs, pagination=orgs)
        return render(request, 'usercenter-fav-org.html', data)


class UserCenterFavTeacherVIew(LoginRequiredMixinView):
    def get(self, request):
        user = request.user
        user_favorite_list = UserFavorite.objects.filter(user=user, fav_type=3)
        teacher_id_list = [user_favorite.fav_id for user_favorite in user_favorite_list]
        teachers = [Teacher.objects.get(id=teacher_id) for teacher_id in teacher_id_list]
        teachers = django_pure_pagination(request, teachers, per_page=1)
        data = dict(teachers=teachers, pagination=teachers)
        return render(request, 'usercenter-fav-teacher.html', data)


class ImageUploadView(LoginRequiredMixinView):
    """
    用户修改头像
    """

    def post(self, request):
        image_upload_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_upload_form.is_valid():
            image_upload_form.save()
            return HttpResponse(success(), content_type='application/json')


class UpdatePwdView(LoginRequiredMixinView):
    """
    修改用户密码
    """

    def post(self, request):
        modify_pwd_form = ModifyPwdForm(request.POST)
        if modify_pwd_form.is_valid():
            password1 = modify_pwd_form.data.get('password1', '')
            password2 = modify_pwd_form.data.get('password2', '')

            if password1 == password2:
                user = request.user
                user.password = make_password(password1)
                user.save()
                return HttpResponse(success(msg='密码修改成功'), content_type='application/json')
            return HttpResponse(fail(msg='两次密码不一致'), content_type='application/json')
        return HttpResponse(json.dumps(modify_pwd_form.errors), content_type='application/json')


class UpdateEmailView(LoginRequiredMixinView):
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return JsonResponse(dict(email='邮箱已注册'))
        send_email(email, send_type='update_email')
        return JsonResponse(dict(status='success'))

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return JsonResponse(dict(status='success'))
        return JsonResponse(dict(email='验证码错误'))


# def page_not_found(request):
#     """
#     全局404处理函数
#     """
#     from django.shortcuts import render_to_response
#     response = render_to_response('404.html')
#     response.status_code = 404
#     return response
#
#
# def page_error(request):
#     """
#     全局500处理函数
#     """
#     from django.shortcuts import render_to_response
#     response = render_to_response('500.html')
#     response.status_code = 500
#     return response
#
#
# def page_forbidden(request):
#     """
#     全局403处理函数
#     """
#     from django.shortcuts import render_to_response
#     response = render_to_response('403.html')
#     response.status_code = 403
#     return response


def bad_request(request, exception, template_name='error/400.html'):
    return render(request, template_name)


def permission_denied(request, exception, template_name='error/403.html'):
    return render(request, template_name)


def page_not_found(request, exception, template_name='error/404.html'):
    return render(request, template_name)


def server_error(request, template_name='error/500.html'):
    return render(request, template_name)

# sql 攻击测试代码
# class LoginUnsafeView(View):
#     def get(self, request):
#         login_form = LoginForm()
#         redirect_to = get_redirect_to(request)  # 获取完整的重定向地址
#         return render(request, 'login.html', {'login_form': login_form, 'redirect_to': redirect_to})
#
#     def post(self, request):
#
#
#         import MySQLdb
#         conn = MySQLdb.connect(host=secure.HOST, port=secure.PORT, user=secure.USER, password=secure.PASSWORD,
#                                db=secure.DATABASE)
#         cursor = conn.cursor()
#
#         user_name = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         sql = "select * from users_userprofile where username='{0}' and password='{1}'".format(user_name, password)
#
#         result = cursor.execute(sql)
#         for raw in cursor.fetchall():  # fetchall()函数可以取到 sql 语句查询到的所有数据
#             print(raw)
#         a = 1
