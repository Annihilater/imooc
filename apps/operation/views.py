import json

from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.views.generic.base import View

from apps.operation.forms import UserAskForm
from apps.operation.models import UserFavorite
from libs.fav_help import reduce_fav_num, add_fav_num
from libs.login import LoginRequiredMixinView


class SearchView(View):
    def get(self, request):
        """
        :param type: 是 js 传过来的参数，名字在 js 里面定义的
        :param keywords: 是 js 传过来的参数，名字在 js 里面定义的
        """
        type = request.GET.get('type', '')
        keywords = request.GET.get('keywords', '')
        url = ''
        if type == 'course':
            url = '/course/'
        if type == 'teacher':
            url = '/teacher/'
        if type == 'org':
            url = '/org/'
        return HttpResponseRedirect("{}?type={}&keywords={}".format(url, type, keywords))


class AddUserAskView(View):
    """
    添加用户咨询
    """

    def post(self, request):
        user_ask_form = UserAskForm(request.POST)

        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)
            status = 'success'
            msg = '提交成功'
        else:
            status = 'fail'
            msg = '提交失败'

        r = dict(status=status, msg=msg)
        r = json.dumps(r)
        return HttpResponse(r, content_type='application/json')


class AddFavView(LoginRequiredMixinView):
    """
    用户收藏、取消收藏
    """

    def post(self, request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))

        if not request.user.is_authenticated:  # 判断用户登录状态
            status = 'fail'
            msg = '用户未登录，收藏失败'
        else:
            exist_record = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if exist_record:  # 如果记录已存在表示用户取消收藏
                exist_record.delete()
                reduce_fav_num(fav_type, fav_id)
                status = 'success'
                msg = '收藏'
            elif fav_id > 0 and fav_type > 0:
                user_fav = UserFavorite(user_id=request.user.id, fav_type=fav_type, fav_id=fav_id)
                user_fav.save()
                add_fav_num(fav_type, fav_id)
                status = 'success'
                msg = '已收藏'
            else:
                status = 'fail'
                msg = '收藏出错'

        r = dict(status=status, msg=msg)
        r = json.dumps(r)
        return HttpResponse(r, content_type='application/json')
