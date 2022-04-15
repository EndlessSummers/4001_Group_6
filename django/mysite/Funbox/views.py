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
                # request.session["user_photo"] = object.user_photo
                try:
                    request.session["user_name"] = object.user_name
                except:
                    request.session["user_name"] = "QaQ"
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
        'body': "to comfirm registration for user: ",
        'url': "/reg_form/",
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
        path = request.get_full_path()
        try:
            email = path.split("email=")[1]
        except:
            return HttpResponse("ERROR: please enter this page through email")
        # print(email)
        return render(request, 'reg_form.html', {"email": email})
    if request.method == "POST":
        # print("jinlaile")
        i_email = request.POST.get("email")
        i_password = request.POST.get("password")
        UserInfo.objects.create(user_id = i_email, password = i_password)
        rep = redirect('/',True)
        return rep

def forget_mail(request, i_email):
    #to do
    user_list = UserInfo.objects.all()
    for object in user_list:
        if object.user_id == i_email:
            subject = 'Funbox Find Password Email'
            current_site = get_current_site(request)
            message = render_to_string('email_template.html', {
                'body': 'to set new password for user: ',
                'url': "/find_password/",
                'user': i_email,
                'domain': current_site.domain,
            })
            send_mail(subject=subject, message=message, from_email= 'Funbox2022@163.com' ,recipient_list = [i_email,])
            status = "success"
            message = "你的邮箱已成功提交"   
            return  JsonResponse({'status':status, 'message':message})
    message = "用户不存在！"
    status = "failure"
    return JsonResponse({'status':status, 'message': message})
# +

def set_profile(request):
    curr_id = request.session.get("user1")
    new_photo = request.FILES.get("photo")
    print("photo is ", new_photo)
    print(request.POST)
    new_name = request.POST.get("name")
    #print(new_name)
    user_list = UserInfo.objects.all()
    for object in user_list:
        if object.user_id == curr_id:
            if new_photo is not None:
                object.user_photo = new_photo
            object.user_name = new_name
            object.save()
            break
    status = "success"
    message = "no message"
    return JsonResponse({"status": status, "message": message})
#+

def user_page(request):
    return render(request, 'userpage.html')

#to do
def change_pswd(request):
    user_info = request.session.get('user1')
    curr_obj = UserInfo.objects.get(user_id = user_info)
    old_password = curr_obj.password
    if (request.POST.get('oldpassword') != old_password):
        status = "failure"
        message = "old password did not match"
        return JsonResponse({'status':status, 'message': message})
    curr_obj.password = request.POST.get("password")
    curr_obj.save()
    status = "success"
    message = "Your password has been changed"
    return JsonResponse({'status':status, 'message': message})

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

def cancel_account(request):
    curr_id = request.session.get("user1")
    cur_obj = UserInfo.objects.get(user_id = curr_id)
    cur_obj.delete()
    return log_out(request)


# ADD_JHIN
def index(request):
    print("views.py.index() called")
    if request.method == "GET":
        status = request.session.get('is_login')
        print("status is:", status)
        if status:
            user_info = request.session.get('user1')
            curr_obj = UserInfo.objects.get(user_id = user_info)
            current_photo = curr_obj.user_photo.url
            print("The url for a photo is ", current_photo)
            current_name = curr_obj.user_name
            pro_style = "display:block;"
            rev_style = "display:none;"
            password_opt = "change password"
            return render(request,'index.html',{"profile_style" : pro_style, "user_email":user_info.split('@')[0], "reverse_style": rev_style, "user_name" : current_name, "user_photo" : current_photo, "password_opt": password_opt })
        else:
            pro_style = "display:none;"
            rev_style = "display:block;"
            password_opt = "forget password"
            return render(request,'index.html',{"profile_style" : pro_style, "reverse_style": rev_style,"password_opt": password_opt }) 
    elif request.method == "POST":
        print("METHOD IS POST")
        # print(request.POST)
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
            return cancel_account(request)
        elif (hint == "forget"):
            # 通过邮箱找回密码
            i_email = request.POST.get("email")
            return forget_mail(request, i_email)
        elif (hint == "profile"):
            print("this is profile")
            return set_profile(request)
        elif (hint == "register"):
            return reg_form(request)
        elif (hint == "change"):
            return change_pswd(request)
        elif (hint == "repeat"):
            return find_password(request)
    else:
        print("NO ENTER")
        return HttpResponse('登录成功')

def project(request):
    print("views.py.project() called")
    if request.method == "GET":
        status = request.session.get('is_login')
        print("status is:", status)
        if status:
            user_info = request.session.get('user1')
            curr_obj = UserInfo.objects.get(user_id = user_info)
            current_photo = curr_obj.user_photo.url
            print("The url for a photo is ", current_photo)
            current_name = curr_obj.user_name
            pro_style = "display:block;"
            rev_style = "display:none;"
            password_opt = "change password"
            return render(request,'project.html',{"profile_style" : pro_style, "user_email":user_info.split('@')[0], "reverse_style": rev_style, "user_name" : current_name, "user_photo" : current_photo, "password_opt": password_opt })
        else:
            pro_style = "display:none;"
            rev_style = "display:block;"
            password_opt = "forget password"
            return render(request,'project.html',{"profile_style" : pro_style, "reverse_style": rev_style,"password_opt": password_opt }) 
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
        status = request.session.get('is_login')
        user_info = request.session.get('user1')
        print("status is:", status)
        if status:
            return render(request, 'windows/window_change_password.html', {"user_email": user_info})
        else:
            return render(request,'windows/window_forget_e.html')

def window_cancel(request):
    if request.method == "GET":
        return render(request,'windows/window_cancel.html')

def window_user(request):
    if request.method == "GET":
        user_info = request.session.get("user1")
        curr_obj = UserInfo.objects.get(user_id = user_info)
        current_photo = curr_obj.user_photo.url
        current_name = curr_obj.user_name
        return render(request,'windows/window_user.html', {"user_email":user_info, "user_name" : current_name, "user_photo" : current_photo })

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

def find_password(request):
    if (request.method == "GET"):
        path = request.get_full_path()
        try:
            email = path.split("email=")[1]
        except:
            return HttpResponse("ERROR: please enter this page through email")
        # print(email)
        return render(request, 'find_password.html', {"email": email})
    if request.method == "POST":
        i_email = request.POST.get("email")
        curr_obj = UserInfo.objects.get(user_id = i_email)
        i_password = request.POST.get("password")
        curr_obj.password = request.POST.get("password")
        curr_obj.save()
        status = "success"
        message = "Your password has been changed"
        return JsonResponse({'status':status, 'message': message})
        