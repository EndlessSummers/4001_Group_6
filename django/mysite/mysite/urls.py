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
#from cookie import views

urlpatterns = [
    path('admin/', admin.site.urls),#系统默认创建的
    path('', views.index), # ADD_JHIN, index page
    # path('', views.index, name="index"), # ADD_JHIN, index page
    path('project/', views.project), # ADD_JHIN, project page
    path('activate/', views.activate, name="activate"),
    path('windows/window_login/', views.window_login),
    path('windows/window_reg_e/', views.window_reg_e),
    path('windows/window_forget_e/', views.window_forget_e),
    path('windows/window_help/', views.window_help),
    path('windows/window_cancel/', views.window_cancel),
    path('windows/window_user/', views.window_user),
    # path('reg_form', views.reg_form),
    path('reg_form/', views.reg_form, name = "reg_form"),
    path("logout/", views.log_out, name="logout"),
]
