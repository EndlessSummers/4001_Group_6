from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect, JsonResponse
import pymysql
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from Funbox.models import UserInfo
from django.core.mail import send_mail
import random

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
# from .tokens import account_activation_token
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
                rep = HttpResponseRedirect('/')
                request.session["is_login"] = True
                request.session["user1"] = object.user_id
                return rep
        message = "user email or password error!"
        status = "failure"
        return JsonResponse({'status':status, 'message': message})
    

def log_out(request):
    try:
        request.session.flush()
        return redirect("/")
    except:
        return redirect("/")
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
def reg_email(request, i_email):
    user_list = UserInfo.objects.all()
    for object in user_list:
        print(object.user_id)
        if object.user_id == i_email:
            message = "用户已存在！"
            status = "failure"
            return JsonResponse({'status':status, 'message': message})
    subject = 'Funbox Activation Email'
    current_site = get_current_site(request)
    message = render_to_string('email_template.html', {
        'user': i_email,
        'domain': current_site.domain,
    })
    send_mail(subject=subject, message=message, from_email= 'Funbox2022@163.com' ,recipient_list = [i_email,])
    status = "success"
    message = "你的邮箱已成功提交"   
    return  JsonResponse({'status':status, 'message':message})
    
#+
def reg_form(request):
    if (request.method == "GET"):
        return render(request, 'reg_form.html')
    if request.method == "POST":
        print("jinlaile")
        i_email = request.POST.get("email")
        i_password = request.POST.get("password")
        UserInfo.objects.create(user_id = i_email, password = i_password)

        rep = redirect('/',True)
        return rep

def forget_mail(i_email):
    #to do
    user_list = UserInfo.objects.all()
    for object in user_list:
        if object.user_id == i_email:
            message = "用户已存在！"
            return JsonResponse({'status':status, 'message': message})
    subject = 'Funbox Activation Email'
    email_message = '''
    This is FUNBOX team. Click here to reset your password
    <br> <a href = ''>Click here </a>
    If the hyperlink is not available, you can copy this to your explorer
    
                                                        Funbox Team
    '''
    send_mail(subject=subject, message= email_message, from_email= 'Funbox2022@163.com' ,recipient_list = [i_email,])
    status = "success"
    message = "你的邮箱已成功提交"   
    return JsonResponse({'status':status, 'message':message})
#+

def set_profile(request):
    curr_id = request.session.get("user1")
    new_photo = request.FILES.get("photo")
    new_name = request.POST.get("name")
    print(new_name)
    user_list = UserInfo.objects.all()
    for object in user_list:
        if object.user_id == curr_id:
            object.user_photo = new_photo
            object.user_name = new_name
            object.save()
    status = "success"
    message = "no message"
    return JsonResponse({"status": status, "message": message})
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


# ADD_JHIN
def index(request):
    print("views.py.index() called")
    if request.method == "GET":
        status = request.session.get('is_login')
        print("status is:", status)
        if status:
            user_info = request.session['user1']
            pro_style = "display:block;"
            rev_style = "display:none;"
            return render(request,'index.html',{"profile_style" : pro_style, "user_email":user_info, "reverse_style": rev_style})
        else:
            pro_style = "display:none;"
            rev_style = "display:block;"
            return render(request,'index.html',{"profile_style" : pro_style, "reverse_style": rev_style}) 
    elif request.method == "POST":
        print("METHOD IS POST")
        print(request.POST)
        hint = request.POST.get('hint')
        if (hint == "email"):
            # 注册时第一次输入邮箱
            i_email = request.POST.get("email")
            print("entered email")
            return reg_email(request, i_email)
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
        elif (hint == "profile"):
            print("this is profile")
            return set_profile(request)
        elif (hint == "register"):
            return reg_form(request)
        
    else:
        print("NO ENTER")
        return HttpResponse('登录成功')

def project(request):
    print("views.py.project() called")
    if request.method == "GET":
        status = request.session.get('is_login')
        print("status is:", status)
        if status:
            user_info = request.session['user1']
            pro_style = "display:block;"
            rev_style = "display:none;"
            return render(request,'project.html',{"profile_style" : pro_style, "user_email":user_info, "reverse_style": rev_style})
        else:
            pro_style = "display:none;"
            rev_style = "display:block;"
            return render(request,'project.html',{"profile_style" : pro_style, "reverse_style": rev_style}) 
    if request.method == "POST":
        user_info = request.session['user1']
        pro_style = "display:block;"
        rev_style = "display:none;"
        return render(request,'project.html',{"profile_style" : pro_style, "user_email":user_info, "reverse_style": rev_style})

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

def activate(request):
    return HttpResponse('Thank you for your email confirmation. Now you can login your account.')

# def reg_email(request):
#     if (request.method == "GET"):
#         return render(request, 'reg_form.html')
        