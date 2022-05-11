from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect, JsonResponse
import pymysql
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from urllib3 import HTTPResponse
from Funbox.models import Activities, UserHash, UserInfo, UserPreference, Notes, notelikes
from django.core.mail import send_mail
import random

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
# from .tokens import account_activation_token
from django.contrib import messages
from django.urls import reverse
from .createData import insert_database
from .recommendation import recommend, stand_est, cos_dis
import numpy as np


# for user login
def login(request, i_email, i_password):
        user_list = UserInfo.objects.all()  #search for all users in the database

        for object in user_list:
            #if the user input fits with any item in database

            if object.user_id == i_email and object.password == i_password:
                
                # redirect to index page, and remember the session
                rep = HttpResponseRedirect('#')
                request.session["is_login"] = True
                request.session["user1"] = object.user_id
                try:
                    request.session["user_name"] = object.user_name
                except:
                    request.session["user_name"] = "QaQ"
                return rep

        # return log in message to the front end
        message = "user email or password error!"
        status = "failure"
        return JsonResponse({'status':status, 'message': message})


# user log out
def log_out(request):
    try:
        # flush the session, and refresh to the index page
        request.session.flush()
        return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect('/')

# cancel the account
def cancel_account(request):

    # get the userid from session and delete from database
    curr_id = request.session.get("user1")
    cur_obj = UserInfo.objects.get(user_id = curr_id)
    cur_obj.delete()

    # note that user logs out automatically
    return log_out(request)


# sending email for user registration 
def reg_email(request, i_email):

    user_list = UserInfo.objects.all()
    # for security, we hash the target link which user clicks

    trans_hash = ""

    # if user already exists in the datbase, actually can not happen
    try: 
        tem_user = UserHash.objects.get(user_id = i_email)
        tem_user.hashnum = str(hash(i_email))
        trans_hash = tem_user.hashnum
        tem_user.save()

    # user doesn't exist. Then hash user email and sore in
    # Userhash class
    except: 
        tem_user = UserHash.objects.create(user_id = i_email)
        tem_user.hashnum = str(hash(i_email))
        trans_hash = tem_user.hashnum
        tem_user.save()

    # add email content and show json response to the user.
    # note that since this is the window of index page, we
    # can only use Ajax to show signals rather than refresh.
    finally:

        for object in user_list:    
            # if user exists in the database, deny the try.
            if object.user_id == i_email:
                message = "用户已存在！"
                status = "failure"
                return JsonResponse({'status':status, 'message': message})
        
        # write the main email body
        subject = 'Funbox Activation Email'
        current_site = get_current_site(request)
        message = render_to_string('email_template.html', {
            'body': "to comfirm registration for user: ",
            'url': "/reg_form/",
            'user': trans_hash,
            'domain': current_site.domain,
            'i_email': i_email,
        })

        # send email to the user and return JsonResponse on the screen
        send_mail(subject=subject, message=message, from_email= 'Funbox2022@163.com' ,recipient_list = [i_email,])
        status = "success"
        message = "Continue to sign up with email sent to your account."
        return  JsonResponse({'status':status, 'message':message})
    

# registration form 
# verify the hash value and registration.
# note that in this and next function,hashing is only used for
# form web address initiating.

def reg_form(request):
    if (request.method == "GET"):
        path = request.get_full_path()
        myuser = ""

        # according to hash value, initiate the original web page address.
        try:
            currhash = path.split("email=")[1]
            tem_user = UserHash.objects.get(hashnum = currhash)
            myuser = tem_user.user_id
        except:
            return HttpResponse("ERROR: Hash value doesn't exist!")
        return render(request, 'reg_form.html', {"email": myuser})

    # according to user input, receive the posted values and save
    # them in the database. after that, return to the index page
    # for user log in.
    if request.method == "POST":
        i_email = request.POST.get("email")
        i_password = request.POST.get("password")
        UserInfo.objects.create(user_id = i_email, password = i_password)
        rep = redirect('/',True)
        return rep


# find password for users
def forget_mail(request, i_email):

    # same procedure as registration. first initiate  
    user_list = UserInfo.objects.all()
    trans_hash = ""

    # hash the address according to user email
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
    
    # write email for finding password and return Json response
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
                message = "Continue to find password with email sent to your account."   
                return  JsonResponse({'status':status, 'message':message})
        message = "用户不存在！"
        status = "failure"
        return JsonResponse({'status':status, 'message': message})

# +

# update user profile including name and photo
def set_profile(request):
    curr_id = request.session.get("user1")

    # record name input and photo input.
    # According to the Django architecture,
    # photos are stored in "media" folder.
    new_photo = request.FILES.get("photo")
    new_name = request.POST.get("name")

    user_list = UserInfo.objects.all()
    for object in user_list:
        if object.user_id == curr_id:
            # only update user photo when a new photo is inserted
            if new_photo is not None:
                object.user_photo = new_photo
            object.user_name = new_name
            object.save()
            break

    # must return something to avoid bugs,
    # however, front end will not use Ajax.
    status = "success"
    message = "no message"
    return JsonResponse({"status": status, "message": message})


# change password when log_in is ture.
def change_pswd(request):
    user_info = request.session.get('user1')
    curr_obj = UserInfo.objects.get(user_id = user_info)
    old_password = curr_obj.password

    # check if input old password corresponds with that in the database.
    if (request.POST.get('oldpassword') != old_password):
        status = "failure"
        message = "old password did not match"
        return JsonResponse({'status':status, 'message': message})
    
    # modify password in the database and return JsonResponse.
    curr_obj.password = request.POST.get("password")
    curr_obj.save()
    status = "success"
    message = "Your password has been changed"
    return JsonResponse({'status':status, 'message': message})


# for filtering activities shown in the index page.
# Each activity will be filled with a "liking" rate 
# according to the input.
# after sorting according to the "liking" rate, the 
# page will be refreshed. Sorted activities will be 
# sent to the front end to display.

def filter_data(request):
    all_act = Activities.objects.all()
    my_dic = {} # this is the dictionary to store user input.
    filter_dic = {} # this is the dictionary to store liking rate for each event.

    # initiate all liking rates of activities to be 0.
    for object in all_act:
        filter_dic[object.activities_id] = 0

    # receive time preference (0-11 hours)
    filter_time = request.POST.get("time")
    if filter_time:
        my_dic["time"] = int(filter_time)
    else:
        my_dic["time"] == 0 # if the time bar is not selected.

    # receive number of participants input
    filter_num = request.POST.get("participant")
    if filter_num:
        my_dic["participant"] = int(filter_num)
    else:
        my_dic["participant"] == 0
    
    # receive home, outdoor and center input.
    filter_home = request.POST.get("Home")
    filter_outdoor = request.POST.get("Outdoor")
    filter_center = request.POST.get("City")

    # receive tag input.
    # If the user clicks it once, it will be fitted with 1 (like)
    # If the user clicks it twice, it will be fitted with -1 (dislike)
    # If the user doesn't click it, it will be fitted with 0 (indifferent)

    my_dic["Film&TV"] = int(request.POST.get("film"))
    my_dic["Game"] = int(request.POST.get("game"))
    my_dic["Music"] = int(request.POST.get("music"))
    my_dic["Cooking"] = int(request.POST.get("cooking"))
    my_dic["Sports"] = int(request.POST.get("sports"))
    my_dic["Handcraft"] = int(request.POST.get("handwork"))

    for obj in all_act:
        
        # if the time suits according to rounding, add liking rate
        if my_dic["time"] == round((obj.activity_timelength)/60):
            filter_dic[obj.activities_id] += 1

        # if the number of participants suits, add liking rate
        if my_dic["participant"] == obj.activity_participant:
            filter_dic[obj.activities_id] += 1

        # if the place suits, add liking rate
        if obj.activity_place in [filter_home, filter_outdoor, filter_center]:
            filter_dic[obj.activities_id] += 1
        
        # in our algorithm we give tag a higher rate. Thus suited tag
        # will be given more liking rates.
        filter_dic[obj.activities_id] += my_dic[obj.activity_tag] * 2

    # sorted according to values. Return the keys.
    newlist = sorted(filter_dic, key = filter_dic.get, reverse= True)

    request.session["sortedlist"] = newlist

    # refresh the index page.
    return redirect("/")
    

# find password according to email
def find_password(request):
    if (request.method == "GET"):

        # get and split the full path.
        path = request.get_full_path()
        try:
            email = path.split("email=")[1]

        # for security, one can only enter this page via email.
        except:
            return HttpResponse("ERROR: please enter this page through email")
        return render(request, 'find_password.html', {"email": email})

    # if the method is post, updatet the database.
    if request.method == "POST":
        i_email = request.POST.get("email")
        curr_obj = UserInfo.objects.get(user_id = i_email)
        i_password = request.POST.get("password")
        curr_obj.password = request.POST.get("password")
        curr_obj.save()
        status = "success"
        message = "Your password has been changed"
        return JsonResponse({'status':status, 'message': message})


# store note information   
def savenotes(request):
    # store the note input
    new_photo = request.FILES.get("photos")
    new_title = request.POST.get("title")
    new_body = request.POST.get("body")
    # store the activity that the note is for
    act_name = request.POST.get("activity")
    act_obj = Activities.objects.get(activities_id = act_name)
    # store the note poster
    user_name = request.session.get("user1")
    user_obj = UserInfo.objects.get(user_id = user_name)
    # store all into database
    Notes.objects.create(user = user_obj, activity = act_obj, title = new_title, note = new_body, activity_photo = new_photo)
    # refresh into activity page
    return redirect("/project/?image=" + act_name)


# verify forum information, enter the main page
# since all operations including register, login, filter... are in index page,
# we pass the request to other functions according to forum.
def index(request):
    
    # for get request
    if request.method == "GET":
        status = request.session.get('is_login')
        data_manage = request.session.get("data")    # this session is used for checking whether activities data is inserted.
        # only in first accessing the webpage will activity database be initialized.
        # otherwise the inserting database code is commented.
        if not data_manage:
            Activities.objects.all().delete()
            insert_database()
            request.session["data"] = 1
        
        # if the activites are filtered
        all_activities = []
        if request.session.get("sortedlist"):
            all_activities_names = request.session.get("sortedlist")
            for item in all_activities_names:
                all_activities.append(Activities.objects.get(activities_id = item))

        # else stay with original orginization
        else:
            all_activities = Activities.objects.all()
        
        # the followings are the interface for front end
        photo_list = []
        desc_list = []
        name_list = []
        for object in all_activities:
            photo_list.append(object.activity_photo.url)
            desc_list.append(object.activity_desc)
            name_list.append(object.activities_id)
        
        # if the user is logged in, the left blank will show his information
        if status:
            user_info = request.session.get('user1')
            curr_obj = UserInfo.objects.get(user_id = user_info)
            current_photo = curr_obj.user_photo.url
            current_name = curr_obj.user_name
            pro_style = "display:block;"
            rev_style = "display:none;"
            password_opt = "change password"
            return render(request,'index.html',{"profile_style" : pro_style, "user_email":user_info.split('@')[0], 
                "reverse_style": rev_style, "user_name" : current_name, "user_photo" : current_photo, "password_opt": password_opt,
                 "images" : photo_list, "names" : name_list})
        
        # else, the left blank will not show user's information
        else:
            pro_style = "display:none;"
            rev_style = "display:block;"
            password_opt = "forget password"
            return render(request,'index.html',{"profile_style" : pro_style, "reverse_style": rev_style,
            "password_opt": password_opt, "images" : photo_list, "names" : name_list }) 
    
    # for post request, the forum depends on "hint" input that is automatically
    # given by the front end. for different "hints" we have different operations.
    elif request.method == "POST":
        
        # receive the invisible hint
        hint = request.POST.get('hint')
        
        # inputting email for registration
        if (hint == "email"):
            i_email = request.POST.get("email")
            return reg_email(request, i_email)
        
        # inputting login information
        elif (hint == "login"):
            i_email = request.POST.get("email")
            i_psd = request.POST.get("password")
            return login(request, i_email, i_psd)

        # cancelling account
        elif (hint == "cancel"):
            return cancel_account(request)

        # forget password
        elif (hint == "forget"):
            i_email = request.POST.get("email")
            return forget_mail(request, i_email)

        # set user profile
        elif (hint == "profile"):
            return set_profile(request)

        # for registration
        elif (hint == "register"):
            return reg_form(request)

        # change password
        elif (hint == "change"):
            return change_pswd(request)

        # find password
        elif (hint == "repeat"):
            return find_password(request)

        # filter activities
        elif (hint == "filter"):
            return filter_data(request)

        # add notes
        elif (hint == "note"):
            return savenotes(request)

    # actually, no else.
    else:
        print("NO ENTER")
        return HttpResponse('登录成功')


# enter detailed activity page
def project(request):
    if request.method == "GET":
        path = request.get_full_path()

        # get the activity that the use is selecting
        try:
            image = path.split("image=")[1]
            curr_act = Activities.objects.get(activities_id = image)
            curr_desc = curr_act.activity_desc
            curr_photo = curr_act.activity_photo.url
            curr_time = curr_act.activity_timelength
            curr_par = curr_act.activity_participant
            curr_place = curr_act.activity_place
            curr_tag = curr_act.activity_tag

        # if no activity selected, use "Hiking" as default
        except:
            curr_act = Activities.objects.get(activities_id = "Hiking")
            image = "Hiking"
            curr_desc = curr_act.activity_desc
            curr_photo = curr_act.activity_photo.url
            curr_time = curr_act.activity_timelength
            curr_par = curr_act.activity_participant
            curr_place = curr_act.activity_place
            curr_tag = curr_act.activity_tag

        # the list of note information for the detailed acivity page.
        note_users = []
        note_titles = []
        note_notes = []
        note_photos = []
        note_ids = []
        note_likes = []
        note_userlike = []
        note_userids = []
        note_userphotos = []

        # if there's note for the activity, load it.
        if Notes.objects.filter(activity = curr_act).count() != 0:
            for i in (Notes.objects.filter(activity = curr_act)):
                note_users.append(i.user.user_name)
                note_titles.append(i.title)
                note_notes.append(i.note)
                note_ids.append(i.id)
                note_likes.append(notelikes.objects.filter(note = i, likes = True).count())
                note_userids.append(i.user.user_id)
                note_userphotos.append(i.user.user_photo.url)

                # null string can't have a url, so we branch it.
                if i.activity_photo == "":
                    note_photos.append("")
                else:
                    note_photos.append(i.activity_photo.url)

        # to load how many likes are for the activity
        likenum = UserPreference.objects.filter(activity = curr_act, likes = True).count()
        # list to be passed for front end
        curr_list = [image, curr_time, curr_par, curr_place, curr_tag, curr_desc,curr_photo, likenum]
        status = request.session.get('is_login')

        # if the user is logged in, left column should contain his information.
        if status:

            user_info = request.session.get('user1')
            curr_obj = UserInfo.objects.get(user_id = user_info)
            current_photo = curr_obj.user_photo.url

            # if the user clicks a like on activity, store it in database.
            if request.GET.get("hint") == "like":
                like_state = request.GET.get("value")
                # if the user and activity doesn't exist in "activity like" table, create it.
                if UserPreference.objects.filter(user = curr_obj, activity = curr_act).count() == 0:
                    UserPreference.objects.create(user = curr_obj, activity = curr_act)
                # modify the "activity like" table
                curr_like = UserPreference.objects.get(user = curr_obj, activity = curr_act)
                if like_state == "1":
                    curr_like.likes = True
                    curr_like.save()
                elif like_state == "-1":
                    curr_like.likes = False
                    curr_like.save()

            # if the user clicks a like on a note, store it in database.
            elif request.GET.get("hint") == "like_note":
                note_state = request.GET.get("value")
                note_id = Notes.objects.get(id = request.GET.get("id"))
                if notelikes.objects.filter(user = curr_obj, note = note_id).count() == 0:
                    notelikes.objects.create(user = curr_obj, note = note_id)
                curr_notelike = notelikes.objects.get(user = curr_obj, note = note_id)
                if note_state == "1":
                    curr_notelike.likes = True
                    curr_notelike.save()
                else:
                    curr_notelike.likes = False
                    curr_notelike.save()

            # parameters passed to front end
            current_name = curr_obj.user_name
            pro_style = "display:block;"
            rev_style = "display:none;"
            password_opt = "change password"

            # parameter passed to front end.
            # if user clicks a like, or already likes the activity/notes,
            # pass the heart parameter to the front end.

            for i in (Notes.objects.filter(activity = curr_act)):
                try:
                    # if user likes that note
                    if notelikes.objects.get(user = curr_obj, note = i).likes == True:
                        note_userlike.append("heart")
                    else:
                        note_userlike.append("")
                except:
                    note_userlike.append("")

            try:
                # if the user likes the activity
                curr_like = UserPreference.objects.get(user = curr_obj, activity = curr_act)
                if curr_like.likes == True:
                    curr_list.append("heart")
                else:
                    curr_list.append("")
            except:
                curr_list.append("")

            return render(request,'project.html',{"profile_style" : pro_style, "user_email":user_info.split('@')[0], "reverse_style": rev_style, "user_name" : current_name, "user_photo" : current_photo, "password_opt": password_opt, 
            "projectlist" : curr_list, "noteusers" : note_users, "notetitles" : note_titles,  "notebodies": note_notes, "notephotos" : note_photos, "noteids" : note_ids, "notehearts" : note_userlike, "notelikes" : note_likes, "userids" : note_userids, "userphotos" : note_userphotos})

        # else if the user is not logged in, he is not allowed
        # to like an activity or note. Also, account information
        # will not be displayed.
        else:
            pro_style = "display:none;"
            rev_style = "display:block;"
            password_opt = "forget password"
            for i in (Notes.objects.filter(activity = curr_act)):
                note_userlike.append("")
            return render(request,'project.html',{"profile_style" : pro_style, "reverse_style": rev_style, "password_opt": password_opt, "projectlist" : curr_list, "noteusers" : note_users, "notetitles" : note_titles,  "notebodies": note_notes, "notephotos" : note_photos, "noteids" : note_ids, "notehearts" : note_userlike, "notelikes" : note_likes, "userids" : note_userids, "userphotos" : note_userphotos}) 
            
    # for all post requests, we pass them into "index" page.
    if request.method == "POST":
        return index(request)


# load help window
def window_help(request):
    if request.method == "GET":
        return render(request,'windows/window_help.html')


# load login window
def window_login(request):
    if request.method == "GET":
        return render(request,'windows/window_login.html')


# load registration email window
def window_reg_e(request):
    if request.method == "GET": 
        return render(request,'windows/window_reg_e.html')


# load find password window
def window_forget_e(request):
    if request.method == "GET":
        status = request.session.get('is_login')
        user_info = request.session.get('user1')
        # check if the user is logged in.
        if status:
            return render(request, 'windows/window_change_password.html', {"user_email": user_info})
        else:
            return render(request,'windows/window_forget_e.html')


# load cancel window
def window_cancel(request):
    if request.method == "GET":
        return render(request,'windows/window_cancel.html')


# load user window
def window_user(request):
    if request.method == "GET":

        # parameters to passed to front end
        user_info = request.session.get("user1")
        curr_obj = UserInfo.objects.get(user_id = user_info)
        current_photo = curr_obj.user_photo.url
        current_name = curr_obj.user_name

        # note that here we need our user similarity recommendation system
        rec_act, likemost = findlikes(user_info)
       
        return render(request,'windows/window_user.html', {"user_email":user_info,
         "user_name" : current_name, "user_photo" : current_photo, "user_recommendations" : rec_act, "user_likes" : likemost })


# load find password window
def find_password(request):

    if (request.method == "GET"):
        path = request.get_full_path()
        myuser = ""
        # get the hash value for user email
        try:
            currhash = path.split("email=")[1]
            tem_user = UserHash.objects.get(hashnum = currhash)
            myuser = tem_user.user_id
        except:
            return HttpResponse("ERROR: Hash value doesn't exist!")
        return render(request, 'find_password.html', {"email": myuser})
    
    # post the user input for new password
    if request.method == "POST":
        i_email = request.POST.get("email")
        curr_obj = UserInfo.objects.get(user_id = i_email)
        i_password = request.POST.get("password")
        curr_obj.password = request.POST.get("password")
        curr_obj.save()
        status = "success"
        message = "Your password has been changed"
        return JsonResponse({'status':status, 'message': message})


# page for submitting note
def note(request):

    if request.method == "GET":
        # to get path is to get current activity
        # if no current activity, "hiking" is used as default.
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

        # if the user is logged in, display information in left column
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

        # else leave blank space in the left column
        else:

            pro_style = "display:none;"
            rev_style = "display:block;"
            password_opt = "forget password"
            return render(request,'note.html',{"profile_style" : pro_style, "reverse_style": rev_style, 
            "password_opt": password_opt, "activity" : image}) 

    elif request.method == "POST":
        return index(request)


# load other users' profile
# this works when someone wants to find the 
# publisher of a note

def window_other(request):
    if request.method == "GET":
        path = request.get_full_path()

        # get user information via get_full_path
        try:
            user_info = path.split("user=")[1]
        except:
            return HTTPResponse("Please enter the page from project!")
        # load the user information and pass to front end
        curr_obj = UserInfo.objects.get(user_id = user_info)
        current_photo = curr_obj.user_photo.url
        current_name = curr_obj.user_name
        rec_act, likemost = findlikes(user_info)
    
        return render(request,'windows/window_other.html', {"user_email":user_info,
         "user_name" : current_name, "user_photo" : current_photo, "user_recommendations" : rec_act, "user_likes" : likemost })

# recommendation system
# including tag that a user likes most
# and the recommended activity by algorithm
def findlikes(user_info):

    tem = 0 # key for user dictionary
    user_dic = {} # consecutive numbers to denote users
    act_dic = {} # consecutive numbers to denote activities
    likedic = {"Music":0, "Film&TV":0, "Game" : 0, "Sports" : 0, "Handcraft" : 0, "Cooking" : 0}    #for likemost tag
    userpos = 0 # object (recommended) user's key in user dictionary

    # initiate user dictionary
    for user in UserInfo.objects.all():
        user_dic[tem] = user
        if user.user_id == user_info:
            userpos = tem
        tem = tem + 1
    tem1 = 0

    # initiate activity dictionary
    for act in Activities.objects.all():
        act_dic[tem1] = act
        tem1 = tem1 + 1
    datalist = []   # store user preference (a 2d array)

    # for each user, add their liking or not to the current list
    for user1 in UserInfo.objects.all():
        curr_list = []
        for act1 in Activities.objects.all():
            try:
                UserPreference.objects.get(user = user1, activity = act1, likes = True)
                curr_list.append(1)
            except:
                curr_list.append(0)
        datalist.append(curr_list)
    
    # np form of datalist
    datalist = np.mat(datalist)

    # recommendation algorithm. Here we use cos_dis and stand_est.
    rec = recommend(datalist, userpos, 1, sim_means=cos_dis, est_method=stand_est)

    # return the name of the recommendation activity
    rec_act = (act_dic[rec[0][0]]).activities_id

    # for each tag, counts its frequency.
    curr_user = UserInfo.objects.get(user_id = user_info)
    for obj in UserPreference.objects.filter(user = curr_user):
        likedic[obj.activity.activity_tag] += 1
    # sorted by value, return key
    likemost = sorted(likedic, key = likedic.get, reverse= True)[0]

    # return recommended activity and most liked tags
    return rec_act, likemost