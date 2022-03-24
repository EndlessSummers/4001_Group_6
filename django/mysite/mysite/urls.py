"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.shortcuts import HttpResponse
import pymysql
from Funbox import views

urlpatterns = [
    path('admin/', admin.site.urls),#系统默认创建的
    path('login/',views.login),#用于打开登录页面
    path('login/reg_email/',views.reg_email),#用于打开注册邮箱
    path('login/input_email/',views.input_email),#用于打开输入邮箱界面
    path('userpage/',views.user_page, name= "userpage"),
    path('userpage/input_changepassword/', views.change_pswd,name = "cg_pswd"),
    path('userpage/input_cancelcheck/', views.cancel_check, name = "cg_cchk"),
    path('login/reg_email/email',views.email, name = "email"), #注册
    path('login/reg_form/', views.reg_form, name = "reg_form"),
    path('login/reg_form/success', views.success, name = "success"),
]
