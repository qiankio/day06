from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect, HttpResponse, render
from django.urls import resolve


class UserInfo(object):
    def __init__(self, role, name, id):
        self.role = role
        self.name = name
        self.id = id
        self.menu_name = None
        self.text_list = []


class AuthMiddleware(MiddlewareMixin):

    def is_white_url(self,request):
        # 1. 不需要登录就可以访问的URL
        if request.path_info in settings.NB_WHITE_URL:
            return True

    def process_request(self, request):
        """校验用户是否登录"""
        if self.is_white_url(request):
            return

        # 2.session中获取用户信息，能获取登录成功；未登录
        # {'role': mapping[role], 'name': user_object.username,'id': user_object.id}
        user_dict = request.session.get(settings.NB_SESSION_KEY)

        # 3.未登录，返回登录界面
        if not user_dict:
            return redirect(settings.NB_LOGIN_URL)

        # 3.用户对象
        request.nb_user = UserInfo(**user_dict)  # 这样子可以直接将user_dict中的参数按照顺序分别给role,name,id
        print(request.nb_user)
        # request.nb_user.id
        # request.nb_user.name
        # request.nb_user.role
        # print(request.nb_user.name)

    def process_view(self, request, callback, callback_args, callback_kwargs):

        if self.is_white_url(request):
            return

        current_name = request.resolver_match.url_name

        # 0.是否是公共权限
        if current_name in settings.NB_PERMISSION_PUBLIC:
            return


        # 1.根据用户角色获取自己所具备的所有权限
        user_permission_dict = settings.NB_PERMISSION[request.nb_user.role]

        # 获取当前用户访问的url
        current_name = request.resolver_match.url_name

        # 判断自己是否有访问的权限
        if current_name not in user_permission_dict:
            # return HttpResponse("你现在不能访问")
            return render(request, "permission.html")

        # 4 有权限
        text_list = []
        text_list.append(user_permission_dict[current_name]["text"])

        menu_name = current_name
        while user_permission_dict[menu_name]["parent"]:
            menu_name = user_permission_dict[menu_name]["parent"]
            text = user_permission_dict[menu_name]["text"]
            text_list.append(text)
        text_list.reverse()
        print(menu_name)

        text_list.append("乾乾的家")

        # 4.1 当前菜单的值
        request.nb_user.menu_name = menu_name

        # 4.2 路径导航
        request.nb_user.text_list = text_list

        print(text_list)