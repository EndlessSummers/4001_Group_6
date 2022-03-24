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
#登录页面
def login(request):
    #指定要访问的页面，render的功能：讲请求的页面结果提交给客户端
    return render(request,'login.html')
#注册页面
def register(request):
    return render(request,'register.html')
#定义一个函数，用来保存注册的数据
def save(request):
    has_register = 0#用来记录当前账号是否已存在，0：不存在 1：已存在
    a = request.GET#获取get()请求
    #print(a)
    #通过get()请求获取前段提交的数据
    user_id = a.get('user_id')
    password = a.get('password')
    #print(user_id,password)
    #连接数据库
    db = pymysql.connect(host = '127.0.0.1', user = 'root',passwd = '51526665',database='mydb')
    #创建游标
    cursor = db.cursor()
    #SQL语句
    sql1 = 'select * from user_info'
    #执行SQL语句
    cursor.execute(sql1)
    #查询到所有的数据存储到all_users中
    all_users = cursor.fetchall()
    i = 0
    while i < len(all_users):
        if user_id in all_users[i]:
            ##表示该账号已经存在
            has_register = 1

        i += 1
    if has_register == 0:
        # 将用户名与密码插入到数据库中
        sql2 = 'insert into user_info(user_id,password) values(%s,%s)'
        cursor.execute(sql2,(user_id,password))
        db.commit()
        cursor.close()
        db.close()
        return HttpResponse('注册成功')
    else:

        cursor.close()
        db.close()
        return HttpResponse('该账号已存在')

def query(request):
    a = request.GET
    user_id = a.get('user_id')
    password = a.get('password')
    user_tup = (user_id,password)
    db = pymysql.connect(host='127.0.0.1',user='root',passwd='51526665',database='mydb')
    cursor = db.cursor()
    sql = 'select * from user_info'
    cursor.execute(sql)
    all_users = cursor.fetchall()
    cursor.close()
    db.close()
    has_user = 0
    i = 0
    while i < len(all_users):
        print(all_users[i][0] + " " + all_users[i][1])
        if user_tup == (all_users[i][0], all_users[i][1]):
            has_user = 1
        i += 1
    if has_user == 1:
        return HttpResponse('登录成功')
    else:
        return HttpResponse('用户名或密码有误')
urlpatterns = [
    path('admin/', admin.site.urls),#系统默认创建的
    path('login/',login),#用于打开登录页面
    path('register/',register),#用于打开注册页面
    path('register/save',save),#输入用户名密码后交给后台save函数处理
    path('login/query',query)#输入用户名密码后交给后台query函数处理

]
