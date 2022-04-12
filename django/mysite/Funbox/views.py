from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import pymysql
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from Funbox.models import UserInfo
from django.core.mail import send_mail

from django.contrib import messages
from django.urls import reverse


# Create your views here.
#登录页面
def login(request, i_email, i_password):
    #指定要访问的页面，render的功能：讲请求的页面结果提交给客户端
        user_list = UserInfo.objects.all()
        for object in user_list:
            print(object.user_id)
            if object.user_id == i_email and object.password == i_password:
                print("success! refresh")
                return render(request, "index.html")
        message = "user email or password error!"
        status = "failure"
        return JsonResponse({'status':status, 'message': message})
    
#+
def input_email(request):
    if request.method == "GET": 
        return render(request,'input_email.html')
    if request.method == "POST":
        i_email = request.POST.get("email")
        user_list = UserInfo.objects.all()
        for object in user_list:
            if object.user_id == i_email:
                return render(request, "email.html")
        message = "用户不存在！"
        # 修改密码的时候
        return render(request, "input_email.html", {"message":message})
                   
#+
def reg_email(i_email):
    user_list = UserInfo.objects.all()
    for object in user_list:
        print(object.user_id)
        if object.user_id == i_email:
            message = "用户已存在！"
            status = "failure"
            return JsonResponse({'status':status, 'message': message})
    subject = 'Funbox Activation Email'
    email_message = '''
    Welcome to Funbox! 
    <br> <a href = ''>Click here </a>
    If the hyperlink is not available, you can copy this to your explorer
    
                                                        Funbox Team
    '''
    send_mail(subject=subject, message= email_message, from_email= 'Funbox2022@163.com' ,recipient_list = [i_email,])
    status = "success"
    message = "你的邮箱已成功提交"   
    return  JsonResponse({'status':status, 'message':message})
    
#+
def reg_form(request):
    if (request.method == "GET"):
        return render(request, 'reg_form.html')
    if request.method == "POST":
        i_email = request.POST.get("email")
        i_password = request.POST.get("password")
        user_list = UserInfo.objects.all()
        flag = 0
        print("hithere")
        for object in user_list:
            print(object.user_id, end='\n')
            if object.user_id == i_email:
                object.password = i_password
                object.save()
                flag = 1
        if flag == 0:
            UserInfo.objects.create(user_id = i_email, password = i_password)
        return render(request, "success.html")

def forget_mail(i_email):
    #to do
    return 1
#+
def user_page(request):
    return render(request, 'userpage.html')

#to do
def change_pswd(request):
    return render(request, 'input_changepassword.html')

#?
def new_pswd(request):
    return render(request, 'input_newpassword.html')

#to do
def cancel_check(request):
    return render(request, 'input_cancelcheck.html')

#?
def pass_email(request):
    return render (request, 'pass_email.html')

#+
def email(request):
    return render (request, 'email.html')

#+
def success(request):
    return render (request, 'success.html')

##数据库：TO DO

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

# ADD_JHIN
def index(request):
    print("views.py.index() called")
    if request.method == "GET":
        print("METHOD IS GET")
        return render(request,'index.html')
    elif request.method == "POST":
        print("METHOD IS POST")
        hint = request.POST['hint']
        if (hint == "email"):
            # 注册时第一次输入邮箱
            i_email = request.POST.get("email")
            print("entered email")
            return reg_email(i_email) 
        elif (hint == "login"):
            i_email = request.POST.get("email")
            i_psd = request.POST.get("password")
            
            # 用户登陆
            print("login ing")
            return login(request, i_email, i_psd)
        elif (hint == "cancel"):
            # 用户注销账户
            print(1)
            return HttpResponse('登录成功')
        elif (hint == "forget_email"):
            # 通过邮箱找回密码
            i_email = request.POST.get("email")
            forget_mail(i_email)
            print(1)
            return HttpResponse('登录成功')
        
    else:
        print("NO ENTER")
        return HttpResponse('登录成功')

def project(request):
    if request.method == "GET":
        return render(request,'project.html')
    if request.method == "POST":
        return render(request,'project.html')

def window_help(request):
    if request.method == "GET":
        return render(request,'windows/window_help.html')

def window_login(request):
    if request.method == "GET":
        return render(request,'windows/window_login.html')

def window_reg_e(request):
    if request.method == "GET": 
        return render(request,'windows/window_reg_e.html')
    
def window_forget_e(request):
    if request.method == "GET":
        return render(request,'windows/window_forget_e.html')
    

def window_cancel(request):
    if request.method == "GET":
        return render(request,'windows/window_cancel.html')

def window_user(request):
    if request.method == "GET":
        return render(request,'windows/window_user.html')

def ajax_submit(request):
    print("AJAX_SUBMIT called")
    if request.method == "GET":
        print("通讯成功GET")
        return JsonResponse({"Info": "通讯成功"})
    elif request.method == "POST":
        print("通讯成功POST")
        return JsonResponse({"Info": "通讯成功"})
    else:
        print("通讯成功NONE")
        return JsonResponse({"Info": "通讯成功"})
        