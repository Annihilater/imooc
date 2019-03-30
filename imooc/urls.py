"""imooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from django.views.static import serve

import xadmin
from apps.operation.views import SearchView
from apps.organization.views import TeacherList, TeacherDetailView
from apps.users.views import RegisterView, ActiveView, ForgetPwdView, RestPwdView, ModifyPwdView, LoginView, IndexView, \
    LogoutView, bad_request, permission_denied, page_not_found, server_error
from imooc.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATIC_ROOT

urlpatterns = [
    path("admin/", xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('active/<activate_code>/', ActiveView.as_view(), name='active'),

    path('forget_password/', ForgetPwdView.as_view(), name='forget_pwd'),
    path('reset/<reset_code>/', RestPwdView.as_view(), name='reset_pwd'),
    path('modify_password/', ModifyPwdView.as_view(), name='modify_pwd'),

    # 验证码 url 配置
    path('captcha', include('captcha.urls')),

    path('search/', SearchView.as_view(), name='search'),

    # 讲师 url 配置
    path('teacher/', TeacherList.as_view(), name='teacher_list'),
    path('teacher/detail/<teacher_id>/', TeacherDetailView.as_view(), name='teacher_detail'),

    # 课程机构 url 配置
    path('org/', include('apps.organization.urls')),
    # path('org/', include(('apps.organization.urls', 'apps.organization'), namespace='org')),

    # 用户 url 配置
    path('user/', include('apps.users.urls')),
    # path('users/', include(('apps.users.urls', 'apps.users'), namespace='users')),

    # 课程 url 配置
    path('course/', include('apps.courses.urls')),
    # path('courses/', include(('apps.courses.urls', 'apps.courses'), namespace='courses')),

    # 用户操作 url 配置
    path('operation/', include('apps.operation.urls')),
    # path('operation/', include(('apps.operation.urls', 'apps.operation'), namespace='operation')),

    # 配置上传文件的访问处理函数，这是视频教程中配置的但是无效，可能 django 版本不同造成的
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 配置静态文件访问 url
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]
# urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
# urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)

# 全局404配置函数
# handler404 = 'users.views.page_not_found'
# handler500 = 'users.views.page_error'
# handler403 = 'users.views.page_forbidden'
handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error
