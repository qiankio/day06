"""day06 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from web.views import account

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', account.login, name="login"),
    path('logout/', account.logout, name="logout"),
    path('sms/login/', account.sms_login, name="sms_login"),

    path('home/', account.home, name="home"),

    path('level/', account.level, name="level"),
    path('order/', account.order, name="order"),
    path('order/add/', account.order_add, name="order_add"),
    path('user/', account.user, name="user"),
]
