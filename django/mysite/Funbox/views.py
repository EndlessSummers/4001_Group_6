from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect, JsonResponse
import pymysql
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from urllib3 import HTTPResponse
from Funbox.models import Activities, UserHash, UserInfo, UserPreference, Notes
from django.core.mail import send_mail
import random

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
# from .tokens import account_activation_token
from django.contrib import messages
from django.urls import reverse
from .createData import insert_database

# Create your views here.
#登录页面
def login(request, i_email, i_password):
    #指定要访问的页面，render的功能：讲请求的页面结果提交给客户端
        user_list = UserInfo.objects.all()
        for object in user_list:
            print(object.user_id)
            if object.user_id == i_email and object.password == i_password:
                print("success! refresh")
                rep = HttpResponseRedirect('#')
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
        return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')

def cancel_account(request):
    curr_id = request.session.get("user1")
    cur_obj = UserInfo.objects.get(user_id = curr_id)
    cur_obj.delete()
    return log_out(request)
# 用户注册发送邮件
# 验证用户不存在，生成HASH值，发送邮件
def reg_email(request, i_email):
    user_list = UserInfo.objects.all()
    trans_hash = ""
    try: 
        tem_user = UserHash.objects.get(user_id = i_email)
        tem_user.hashnum = str(hash(i_email))
        trans_hash = tem_user.hashnum
        tem_user.save()
    except: 
        tem_user = UserHash.objects.create(user_id = i_email)
        tem_user.hashnum = str(hash(i_email))
        trans_hash = tem_user.hashnum
        tem_user.save()
    finally:
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
            'user': trans_hash,
            'domain': current_site.domain,
            'i_email': i_email,
        })
        send_mail(subject=subject, message=message, from_email= 'Funbox2022@163.com' ,recipient_list = [i_email,])
        status = "success"
        message = "你的邮箱已成功提交"
        return  JsonResponse({'status':status, 'message':message})
    
# 用户注册表单
# 验证HASH值，生成网页，注册
def reg_form(request):
    if (request.method == "GET"):
        path = request.get_full_path()
        myuser = ""
        try:
            currhash = path.split("email=")[1]
            tem_user = UserHash.objects.get(hashnum = currhash)
            myuser = tem_user.user_id
        except:
            return HttpResponse("ERROR: Hash value doesn't exist!")
        # print(email)
        return render(request, 'reg_form.html', {"email": myuser})
    if request.method == "POST":
        # print("jinlaile")
        i_email = request.POST.get("email")
        i_password = request.POST.get("password")
        UserInfo.objects.create(user_id = i_email, password = i_password)
        rep = redirect('/',True)
        return rep

# 用户找回密码
# 验证用户存在，生成HASH值，发送邮件
def forget_mail(request, i_email):
    #to do
    user_list = UserInfo.objects.all()
    trans_hash = ""
    try: 
        tem_user = UserHash.objects.get(user_id = i_email)
        tem_user.hashnum = str(hash(i_email))
        trans_hash = tem_user.hashnum
        tem_user.save()
    except: 
        tem_user = UserHash.objects.create(user_id = i_email)
        tem_user.hashnum = str(hash(i_email))
        trans_hash = tem_user.hashnum
        tem_user.save()
    finally:
        for object in user_list:
            print(object.user_id)
            if object.user_id == i_email:
                subject = 'Funbox Find Password Email'
                current_site = get_current_site(request)
                message = render_to_string('email_template.html', {
                    'body': 'to set new password for user: ',
                    'url': "/find_password/",
                    'user': trans_hash,
                    'domain': current_site.domain,
                    'i_email': i_email,
                })
                send_mail(subject=subject, message=message, from_email= 'Funbox2022@163.com' ,recipient_list = [i_email,])
                status = "success"
                message = "你的邮箱已成功提交"   
                return  JsonResponse({'status':status, 'message':message})
        message = "用户不存在！"
        status = "failure"
        return JsonResponse({'status':status, 'message': message})
# +

# 用户修改用户名，修改头像 "profile"
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
    # BUGGY
    status = "success"
    message = "no message"
    return JsonResponse({"status": status, "message": message})

# 登陆状态修改密码 "change"
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

# 过滤函数
# 返回排序后图片列表 "filter"
def filter_data(request):
    all_act = Activities.objects.all()
    my_dic = {}
    filter_dic = {}
    # print(request.POST)
    for object in all_act:
        filter_dic[object.activities_id] = 0
        print(object.activities_id)

    filter_time = request.POST.get("time")
    if filter_time:
        my_dic["time"] = int(filter_time)
    else:
        my_dic["time"] == 0

    filter_num = request.POST.get("participant")
    if filter_num:
        my_dic["participant"] = int(filter_num)
    else:
        my_dic["participant"] == 0
    
    filter_home = request.POST.get("Home")
    filter_outdoor = request.POST.get("Outdoor")
    filter_center = request.POST.get("City")

    my_dic["Film&TV"] = int(request.POST.get("film"))
    my_dic["Game"] = int(request.POST.get("game"))
    my_dic["Music"] = int(request.POST.get("music"))
    my_dic["Cooking"] = int(request.POST.get("cooking"))
    my_dic["Sports"] = int(request.POST.get("sports"))
    my_dic["Handcraft"] = int(request.POST.get("handwork"))

    for obj in all_act:
        print(obj.activities_id)
        if my_dic["time"] == round((obj.activity_timelength)/60):
            filter_dic[obj.activities_id] += 1

        if my_dic["participant"] == obj.activity_participant:
            filter_dic[obj.activities_id] += 1
        if obj.activity_place in [filter_home, filter_outdoor, filter_center]:
            filter_dic[obj.activities_id] += 1
        print(obj.activities_id, filter_dic[obj.activities_id])
        filter_dic[obj.activities_id] += my_dic[obj.activity_tag] * 2
    print(filter_dic)
    newlist = sorted(filter_dic, key = filter_dic.get, reverse= True)
    print(newlist)
    request.session["sortedlist"] = newlist

    return redirect("/")

# 通过邮件找回密码
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

# 创建数据库
       
def savenotes(request):
    new_photo = request.FILES.get("photos")
    new_title = request.POST.get("title")
    new_body = request.POST.get("body")
    act_name = request.POST.get("activity")
    act_obj = Activities.objects.get(activities_id = act_name)
    user_name = request.session.get("user1")
    user_obj = UserInfo.objects.get(user_id = user_name)
    Notes.objects.create(user = user_obj, activity = act_obj, title = new_title, note = new_body, activity_photo = new_photo)
    return redirect("/project/?image=" + act_name)

# 验证表单信息 进入首页
def index(request):
    print("views.py.index() called")
    if request.method == "GET":
        status = request.session.get('is_login')
        data_manage = request.session.get("data")
        if not data_manage:
            #Activities.objects.all().delete()
            #insert_database()
            request.session["data"] = 1
        
        all_activities = []
        if request.session.get("sortedlist"):
            all_activities_names = request.session.get("sortedlist")
            for item in all_activities_names:
                all_activities.append(Activities.objects.get(activities_id = item))
            
        else:
            all_activities = Activities.objects.all()
        photo_list = []
        desc_list = []
        name_list = []
        for object in all_activities:
            photo_list.append(object.activity_photo.url)
            desc_list.append(object.activity_desc)
            name_list.append(object.activities_id)
        print(photo_list)
        if status:
            user_info = request.session.get('user1')
            curr_obj = UserInfo.objects.get(user_id = user_info)
            current_photo = curr_obj.user_photo.url
            print("The url for a photo is ", current_photo)
            current_name = curr_obj.user_name
            pro_style = "display:block;"
            rev_style = "display:none;"
            password_opt = "change password"
            return render(request,'index.html',{"profile_style" : pro_style, "user_email":user_info.split('@')[0], 
                "reverse_style": rev_style, "user_name" : current_name, "user_photo" : current_photo, "password_opt": password_opt,
                 "images" : photo_list, "names" : name_list})
        else:
            pro_style = "display:none;"
            rev_style = "display:block;"
            password_opt = "forget password"
            return render(request,'index.html',{"profile_style" : pro_style, "reverse_style": rev_style,
            "password_opt": password_opt, "images" : photo_list, "names" : name_list }) 
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
        elif (hint == "filter"):
            return filter_data(request)
        elif (hint == "note"):
            return savenotes(request)
    else:
        print("NO ENTER")
        return HttpResponse('登录成功')

# 进入工程页
def project(request):
    print("views.py.project() called")
    if request.method == "GET":
        path = request.get_full_path()
        try:
            image = path.split("image=")[1]
            curr_act = Activities.objects.get(activities_id = image)
            curr_desc = curr_act.activity_desc
            curr_photo = curr_act.activity_photo.url
            curr_time = curr_act.activity_timelength
            curr_par = curr_act.activity_participant
            curr_place = curr_act.activity_place
            curr_tag = curr_act.activity_tag
     
        except:
            curr_act = Activities.objects.get(activities_id = "Hiking")
            image = "Hiking"
            curr_desc = curr_act.activity_desc
            curr_photo = curr_act.activity_photo.url
            curr_time = curr_act.activity_timelength
            curr_par = curr_act.activity_participant
            curr_place = curr_act.activity_place
            curr_tag = curr_act.activity_tag
        
        print("I'm back")
        like_state = request.GET.get("value")
        print("like state: ", like_state)

        note_users = []
        note_titles = []
        note_notes = []
        note_photos = []


        if Notes.objects.filter(activity = curr_act).count() != 0:
            for i in (Notes.objects.filter(activity = curr_act)):
                note_users.append(i.user.user_id)
                note_titles.append(i.title)
                note_notes.append(i.note)
                if i.activity_photo == None:
                    note_photos.append(None)
                else:
                    note_photos.append(i.activity_photo.url)


        likenum = UserPreference.objects.filter(activity = curr_act, likes = True).count()
        curr_list = [image, curr_time, curr_par, curr_place, curr_tag, curr_desc,curr_photo, likenum]
        status = request.session.get('is_login')
        print("status is:", status)
        if status:

            user_info = request.session.get('user1')
            curr_obj = UserInfo.objects.get(user_id = user_info)
            current_photo = curr_obj.user_photo.url
        
            if UserPreference.objects.filter(user = curr_obj, activity = curr_act).count() == 0:
                print("created again for ", curr_obj.user_id)
                UserPreference.objects.create(user = curr_obj, activity = curr_act)
            curr_like = UserPreference.objects.get(user = curr_obj, activity = curr_act)
            if like_state == "1":

                curr_like.likes = True
                curr_like.save()
            elif like_state == "-1":
                curr_like.likes = False
                curr_like.save()

            current_name = curr_obj.user_name
            pro_style = "display:block;"
            rev_style = "display:none;"
            password_opt = "change password"
            if curr_like.likes == True:
                curr_list.append("heart")
            else:
                curr_list.append("")
            return render(request,'project.html',{"profile_style" : pro_style, "user_email":user_info.split('@')[0], "reverse_style": rev_style, "user_name" : current_name, "user_photo" : current_photo, 
            "password_opt": password_opt, "projectlist" : curr_list, "noteusers" : note_users,
            "notetitles" : note_titles,  "notebodies": note_notes, "notephotos" : note_photos})
        else:
            # if (like_state != None):
                #弹出一个框
            pro_style = "display:none;"
            rev_style = "display:block;"
            password_opt = "forget password"
            return render(request,'project.html',{"profile_style" : pro_style, "reverse_style": rev_style, 
            "password_opt": password_opt, "projectlist" : curr_list, "noteusers" : note_users,
            "notetiles" : note_titles,  "notebodies": note_notes, "notephotos" : note_photos}) 
            
    if request.method == "POST":
        print("METHOD IS POST")
        return index(request)

# 加载help窗口
def window_help(request):
    if request.method == "GET":
        return render(request,'windows/window_help.html')

# 加载login窗口
def window_login(request):
    if request.method == "GET":
        return render(request,'windows/window_login.html')

# 加载注册email窗口
def window_reg_e(request):
    if request.method == "GET": 
        return render(request,'windows/window_reg_e.html')
    
# 加载找回密码email窗口
def window_forget_e(request):
    if request.method == "GET":
        status = request.session.get('is_login')
        user_info = request.session.get('user1')
        print("status is:", status)
        if status:
            return render(request, 'windows/window_change_password.html', {"user_email": user_info})
        else:
            return render(request,'windows/window_forget_e.html')

# 加载cancel窗口
def window_cancel(request):
    if request.method == "GET":
        return render(request,'windows/window_cancel.html')

# 加载user窗口
def window_user(request):
    if request.method == "GET":
        user_info = request.session.get("user1")
        curr_obj = UserInfo.objects.get(user_id = user_info)
        current_photo = curr_obj.user_photo.url
        current_name = curr_obj.user_name
        return render(request,'windows/window_user.html', {"user_email":user_info, "user_name" : current_name, "user_photo" : current_photo })


def find_password(request):
    if (request.method == "GET"):
        path = request.get_full_path()
        myuser = ""
        try:
            currhash = path.split("email=")[1]
            tem_user = UserHash.objects.get(hashnum = currhash)
            myuser = tem_user.user_id
        except:
            return HttpResponse("ERROR: Hash value doesn't exist!")
        # print(email)
        return render(request, 'find_password.html', {"email": myuser})
    if request.method == "POST":
        i_email = request.POST.get("email")
        curr_obj = UserInfo.objects.get(user_id = i_email)
        i_password = request.POST.get("password")
        curr_obj.password = request.POST.get("password")
        curr_obj.save()
        status = "success"
        message = "Your password has been changed"
        return JsonResponse({'status':status, 'message': message})

def note(request):
    if request.method == "GET":
        path = request.get_full_path()
        try:
            image = path.split("image=")[1]
            curr_act = Activities.objects.get(activities_id = image)
            curr_desc = curr_act.activity_desc
            curr_photo = curr_act.activity_photo.url
            curr_time = curr_act.activity_timelength
            curr_par = curr_act.activity_participant
            curr_place = curr_act.activity_place
            curr_tag = curr_act.activity_tag
     
        except:
            curr_act = Activities.objects.get(activities_id = "Hiking")
            image = "Hiking"
            curr_desc = curr_act.activity_desc
            curr_photo = curr_act.activity_photo.url
            curr_time = curr_act.activity_timelength
            curr_par = curr_act.activity_participant
            curr_place = curr_act.activity_place
            curr_tag = curr_act.activity_tag

        status = request.session.get('is_login')

        if status:

            user_info = request.session.get('user1')
            curr_obj = UserInfo.objects.get(user_id = user_info)
            current_photo = curr_obj.user_photo.url

            current_name = curr_obj.user_name
            pro_style = "display:block;"
            rev_style = "display:none;"
            password_opt = "change password"

            return render(request,'note.html',{"profile_style" : pro_style, "user_email":user_info.split('@')[0], "reverse_style": rev_style, "user_name" : current_name, "user_photo" : current_photo, 
            "password_opt": password_opt, "activity" : image})
        else:

            pro_style = "display:none;"
            rev_style = "display:block;"
            password_opt = "forget password"
            return render(request,'note.html',{"profile_style" : pro_style, "reverse_style": rev_style, 
            "password_opt": password_opt, "activity" : image}) 
    elif request.method == "POST":
        return index(request)
        
