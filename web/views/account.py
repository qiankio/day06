from django.shortcuts import render, redirect
from web import models

from utils.encrypt import md5

# 1.定义类
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings


class LoginForm(forms.Form):
    role = forms.ChoiceField(
        required=True,
        choices=(("2", "客户"), ("1", "管理员")),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码"}, render_value=True)
    )


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    # 1.接收并获取数据(数据格式或是否为空验证 - Form组件 & ModelForm组件）
    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, "login.html", {"form": form})

    # {'role': '1', 'username': 'asdfasdf', 'password': '123123'}
    # print(form.cleaned_data)  # {"username":'',"password":'xxx","role":xxx}
    role = form.cleaned_data.get("role")
    username = form.cleaned_data.get("username")
    password = form.cleaned_data.get("password")
    password = md5(password)

    # 2.去数据库校验  1管理员  2客户
    mapping = {"1": "ADMIN", "2": "CUSTOMER"}
    if role not in mapping:
        return render(request, "login.html", {'form': form, 'error': "角色不存在"})

    if role == "1":
        user_object = models.Administrator.objects.filter(active=1, username=username, password=password).first()
    else:
        user_object = models.Customer.objects.filter(active=1, username=username, password=password).first()
        print(user_object, "开始校验了")

    # 2.1 校验失败
    if not user_object:
        form.add_error("username", "用户名或密码错误")
        return render(request, "login.html", {'form': form})

    # 2.2 校验成功，用户信息写入session+进入项目后台
    mapping = {"1": "ADMIN", "2": "CUSTOMER"}
    # request.session["user_info"] = {'role': mapping[role], "name": user_object.username, "id": user_object.id}
    request.session[settings.NB_SESSION_KEY] = {'role': mapping[role], 'name': user_object.username,
                                                'id': user_object.id}
    print("我到这里了")
    return redirect(settings.LOGIN_HOME)


def sms_login(request):
    # return render(request, "sms_login.html")
    pass


def sms_send(request):
    pass


def logout(request):
    """注销"""
    request.session.clear()
    return render(settings.NB_LOGIN_URL)


def home(request):
    return render(request, 'home.html')


def level(request):
    return render(request, "level.html")


def order(request):
    return render(request, "order.html")

def order_add(request):
    return render(request, "order_add.html")


def user(request):
    return render(request, "user.html")
