from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseRedirect, JsonResponse
import pymysql
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from Funbox.models import Activities, UserInfo
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
                   
# 用户注册发送邮件
# 验证用户不存在，生成HASH值，发送邮件
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
    
# 用户注册表单
# 验证HASH值，生成网页，注册
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

# 用户找回密码
# 验证用户存在，生成HASH值，发送邮件
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
def insert_database():
    Activities.objects.create(activities_id = "Cake",
    activity_desc = "Cake is an ancient pastry, usually made in an oven. The cake is made of eggs, sugar and wheat flour as the main raw materials. With milk, fruit juice, milk powder, fragrant powder, salad oil, water, shortening, baking powder as accessories. After stirring, mixing, and baking, a sponge-like snack is created.",
    activity_timelength = 30,  # Field name made lowercase.
    activity_photo = "/photos_activities/Cake.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Cooking")
    
    Activities.objects.create(activities_id = "Baguette",
    activity_desc = "Baguette (French: /ba.ɡɛt/, English: /bæ'gɛt/) is one of the most traditional French breads and is rich in nutrients. The representative of French bread is 'baguette', baguette originally means a long gem.",
    activity_timelength = 180,  # Field name made lowercase.
    activity_photo = "/photos_activities/Baguette.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Cooking")

    Activities.objects.create(activities_id = "Script_Kill",
    activity_desc = "'Script Kill', the term originated from the Western banquet live role-playing 'Murder Mystery', is a project where players go to a live venue to experience a reasoning project. The rule of script killing is that players first select a character, read the script corresponding to the character, and collect clues to find the real murderer hidden in the activity. [1] [10] Script Killing is not only a game, but also an entertainment project that integrates knowledge attributes, psychological game attributes, and strong social attributes.",
    activity_timelength = 360,  # Field name made lowercase.
    activity_photo = "/photos_activities/Script_Kill.jpg",
    activity_participant = 8,
    activity_place = "Home",
    activity_tag = "Game")

    Activities.objects.create(activities_id = "Texas_hold_em",
    activity_desc = "Texas Hold 'em is a card game, can be multiplayer participation, its gameplay is, the player each issued two hole cards, the desktop in turn issued 5 public cards, the player with their own two hole cards and 5 public cards free combination, according to the size of the decision.",
    activity_timelength = 120,  # Field name made lowercase.
    activity_photo = "/photos_activities/Texas_hold_em.jpg",
    activity_participant = 6,
    activity_place = "Home",
    activity_tag = "Game")

    Activities.objects.create(activities_id = "Avalon",
    activity_desc = "Avalon, formerly known as Avalon, usually requires 5-10 people to participate, is a casual puzzle game suitable for party dating and verbal reasoning.",
    activity_timelength = 240,  # Field name made lowercase.
    activity_photo = "/photos_activities/Avalon.jpg",
    activity_participant = 7,
    activity_place = "Home",
    activity_tag = "Game")

    Activities.objects.create(activities_id = "Spider_Man_No_Way_Home",
    activity_desc = "'Spider-Man: Homeless Heroes' is the end of the hero series trilogy, and also marks the official opening of the Marvel multiverse. This time, Spider-Man and Doctor Strange joined forces to start a time-space melee again after 'Avengers 4'. Spider-Man uses Doctor Strange's ability to manipulate time and space to open the passage of time and space, causing an unprecedented crisis.",
    activity_timelength = 148,  # Field name made lowercase.
    activity_photo = "/photos_activities/Spider_Man_No_Way_Home.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Film&TV")

    Activities.objects.create(activities_id = "LAVAIOXISEA",
    activity_desc = "Alien Theme Music Album",
    activity_timelength = 20,  # Field name made lowercase.
    activity_photo = "/photos_activities/LAVAIOXISEA.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Music")

    Activities.objects.create(activities_id = "Basketball",
    activity_desc = "Basketball is a physical confrontation sport centered on the hands, and it is the core event of the Olympic Games.",
    activity_timelength = 180,  # Field name made lowercase.
    activity_photo = "/photos_activities/Basketball.jpg",
    activity_participant = 6,
    activity_place = "Outdoor",
    activity_tag = "Sports")

    Activities.objects.create(activities_id = "Hiking",
    activity_desc = "Trekking (Tramp) refers to the purpose of walking exercises in the suburbs of the city, rural areas or mountains, hiking is the most typical and common outdoor sports. Because short-distance hiking is relatively simple, it does not require too much skill and equipment, and is often considered a leisure activity.",
    activity_timelength = 480,  # Field name made lowercase.
    activity_photo = "/photos_activities/Hiking.jpg",
    activity_participant = 2,
    activity_place = "Outdoor",
    activity_tag = "Sports")

    Activities.objects.create(activities_id = "Wood",
    activity_desc = "Carpentry, is a craft, a unique technology, is also a commonly used technology in architecture, is one of the three elements of traditional Chinese (that is, carpentry, wood, carpenter). It is said that in ancient times, houses were built, and on the day the house was built, it was necessary to ask a carpenter to suppress evil!",
    activity_timelength = 180,  # Field name made lowercase.
    activity_photo = "/photos_activities/Wood.jpg",
    activity_participant = 2,
    activity_place = "Center",
    activity_tag = "Handcraft")

    Activities.objects.create(activities_id = "Pottery",
    activity_desc = "Ceramic art, broadly speaking, is an art form that combines traditional Chinese ancient culture with modern art. It can be seen from the historical development that 'ceramic art' is a comprehensive art, which has experienced a complex and long process of cultural accumulation. It has an inseparable relationship of inheritance and comparison with painting, sculpture, design, and other arts and crafts.",
    activity_timelength = 120,  # Field name made lowercase.
    activity_photo = "/photos_activities/Pottery.jpg",
    activity_participant = 1,
    activity_place = "Center",
    activity_tag = "Handcraft")

    Activities.objects.create(activities_id = "Origami",
    activity_desc = "Origami is an artistic activity in which paper is folded into various shapes. Origami is not limited to just using paper. Origami lovers around the world have used a variety of materials, such as tin foil, napkins, acetate sheets, etc., while adhering to folding norms",
    activity_timelength = 30,  # Field name made lowercase.
    activity_photo = "/photos_activities/Origami.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Handcraft")

    Activities.objects.create(activities_id = "Football",
    activity_desc = 'The predecessor of modern football originated from the ball game "Cuju" in Zizhou, Shandong (now Zibo City) in ancient China. Later, it was spread from China to Europe by the Arabs and gradually evolved into modern football. Modern football started in England.',
    activity_timelength = 240,  # Field name made lowercase.
    activity_photo = "/photos_activities/Football.jpg",
    activity_participant = 12,
    activity_place = "Outdoor",
    activity_tag = "Sports")

    Activities.objects.create(activities_id = "Punk",
    activity_desc = "Music Festival album",
    activity_timelength = 60,  # Field name made lowercase.
    activity_photo = "/photos_activities/Punk.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Music")

    Activities.objects.create(activities_id = "Turning_Red",
    activity_desc = "Xiaomei, a 13-year-old girl, grew up in a typical Asian family that runs an ancestral hall open to the public as a tourist attraction and enshrines the ancestors of the family. Xiaomei's mother is a caring and slightly neurotic woman who cares for her children, in front of her mother, Xiaomei always plays the role of a well-behaved woman, but in fact, Xiaomei, like all children of the same age, is naughty, active, and begins to be interested in the opposite sex. ",
    activity_timelength = 100,  # Field name made lowercase.
    activity_photo = "/photos_activities/Turning_Red.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Film&TV")

    Activities.objects.create(activities_id = "Toast",
    activity_desc = "Bread baked with a lid is sliced and squared, and sandwiched with ham or vegetables is sandwiched. The bread baked without a lid is rectangular and topped, resembling a large rectangular loaf of bread.",
    activity_timelength = 180,  # Field name made lowercase.
    activity_photo = "/photos_activities/Toast.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Cooking")

    Activities.objects.create(activities_id = "Yangzhou_fried_rice",
    activity_desc = "Egg fried rice is a common dish. The earliest records are found in 1972 in 1972 in Changsha, Hunan Province, on the bamboo tablets excavated from the Mawangdui Han Tomb. According to expert research, it is a food made of sticky rice and eggs. Some people speculate that this may be the predecessor of egg fried rice.",
    activity_timelength = 20,  # Field name made lowercase.
    activity_photo = "/photos_activities/Yangzhou_fried_rice.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Cooking")

    Activities.objects.create(activities_id = "Braised_prawns_in_oil",
    activity_desc = "Braised prawns in oil is a famous dish in Shandong Province, which belongs to Lu cuisine; the main ingredient of this dish is the large shrimp of Bohai Bay before the Qingming Dynasty, using the unique oil braising technique of Lu cuisine. This is a famous dish with a long history, and the four flavors of fresh, sweet and salty complement each other, and the aftertaste is endless. In recent years, the popular oil braised prawns are from Hubei Qianjiang's Ecai, which is made using freshwater shrimp (commonly known as crayfish), which is different from the oil-braised prawns of Lucai.",
    activity_timelength = 45,  # Field name made lowercase.
    activity_photo = "/photos_activities/Braised_prawns_in_oil.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Cooking")

    Activities.objects.create(activities_id = "Japanese_food",
    activity_desc = "Japanese cuisine originated in the Japanese archipelago and has gradually developed into a dish with unique Japanese characteristics. Japanese Japanese food requirements: natural ingredients, bright colors, diverse utensils, creating a visual sense of high-quality, and materials and conditioning methods also need to pay attention to seasonal changes, a dish needs to adapt to the seasons to use different cooking methods and presentation.",
    activity_timelength = 120,  # Field name made lowercase.
    activity_photo = "/photos_activities/Japanese_food.jpg",
    activity_participant = 2,
    activity_place = "Center",
    activity_tag = "Cooking")

    Activities.objects.create(activities_id = "Korean_food",
    activity_desc = "Koreans are generally divided into home-cooked dishes and feast dishes, each with its own flavor, spicy and fresh flavor, and many ingredients, no matter what kind of kimchi or kimchi flavor seasoning is a must-have dish in Korean cuisine. Traditional Korean food mostly takes the form of set food or rice bed, focuses on one juice and three dishes, and likes to grill meat, which also influenced the Asuka era cuisine of neighboring Japan during the Baekje period.",
    activity_timelength = 120,  # Field name made lowercase.
    activity_photo = "/photos_activities/Korean_food.jpg",
    activity_participant = 2,
    activity_place = "Center",
    activity_tag = "Cooking")

    Activities.objects.create(activities_id = "Hotpot",
    activity_desc = " pot generally refers to the cooking method of using the pot as a utensil, burning the pot with a heat source, and boiling water or soup to cook all kinds of food, and can also refer to the pot and pan used in this cooking method. It is characterized by eating while cooking, or the pot itself has a thermal insulation effect, and the food is still steaming when eating, and the soup is one.",
    activity_timelength = 120,  # Field name made lowercase.
    activity_photo = "/photos_activities/Hotpot.jpg",
    activity_participant = 2,
    activity_place = "Center",
    activity_tag = "Cooking")

    Activities.objects.create(activities_id = "Jigsaw_puzzle",
    activity_desc = "Jigsaw puzzles are a popular type of intellectual game, with many variations and varying levels of difficulty.",
    activity_timelength = 600,  # Field name made lowercase.
    activity_photo = "/photos_activities/Jigsaw_puzzle.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Handcraft")

    Activities.objects.create(activities_id = "Lego",
    activity_desc = "Lego bricks are children's favorite toys. This plastic building block has bumps on one end and holes on the other end that can be inserted into the bumps. There are more than 1,300 shapes, and each shape has 12 different colors, mainly red, yellow, blue, white, and green. It relies on children to use their own brains, and can create endlessly changing shapes.",
    activity_timelength = 480,  # Field name made lowercase.
    activity_photo = "/photos_activities/Lego.jpg",
    activity_participant = 2,
    activity_place = "Center",
    activity_tag = "Handcraft")

    Activities.objects.create(activities_id = "Shadow_puppetry",
    activity_desc = 'Shadow puppetry is an ancient traditional Chinese folk art. Old Beijingers call it "donkey shadow play". According to historical records, shadow play began in the Western Han Dynasty, flourished in the Tang Dynasty, flourished in the Qing Dynasty, and spread to West Asia and Europe during the Yuan Dynasty. It has a long history and a long history.',
    activity_timelength = 180,  # Field name made lowercase.
    activity_photo = "/photos_activities/Shadow_puppetry.jpg",
    activity_participant = 6,
    activity_place = "Home",
    activity_tag = "Handcraft")

    Activities.objects.create(activities_id = "Housework",
    activity_desc = 'Daily life affairs of the family. The language "Liang Shu·Zhang Su Zhuan": "Zhi is addicted to alcohol, forgives everything, and especially forgets about housework."',
    activity_timelength = 120,  # Field name made lowercase.
    activity_photo = "/photos_activities/Housework.jpg",
    activity_participant = 3,
    activity_place = "Home",
    activity_tag = "Handcraft")

    Activities.objects.create(activities_id = "Dough_figurine",
    activity_desc = 'Dough figurine is a kind of Chinese folk handicraft that is simple to make but highly artistic. The art of dough sculpture in China has been recorded in writing as early as the Han Dynasty. It uses flour and glutinous rice flour as the main raw materials, plus color, paraffin, honey and other ingredients, and is processed to prevent cracking and mildew to make soft dough of various colors.',
    activity_timelength = 60,  # Field name made lowercase.
    activity_photo = "/photos_activities/Dough_figurine.jpg",
    activity_participant = 2,
    activity_place = "Center",
    activity_tag = "Handcraft")

    Activities.objects.create(activities_id = "Suger_figurine",
    activity_desc = 'Blowing suger is an industry in Beijing in the old days. The hawkers walk the streets and alleys shoulder-to-shoulder. At one end of the pick is a rectangular cabinet with a shelf. Below the cabinet is a semi-circular open wooden cage with a small charcoal stove inside. A large spoon on the stove is full of Syrup (which is obtained by dissolving maltose).',
    activity_timelength = 60,  # Field name made lowercase.
    activity_photo = "/photos_activities/Suger_figurine.jpg",
    activity_participant = 4,
    activity_place = "Center",
    activity_tag = "Handcraft")

    Activities.objects.create(activities_id = "Coding",
    activity_desc = 'Programming is the process of letting computer code solve a problem, specifying a certain computing method for a computing system, making the computing system run according to the computing method, and finally getting the corresponding result.',
    activity_timelength = 300,  # Field name made lowercase.
    activity_photo = "/photos_activities/Coding.jpg",
    activity_participant = 4,
    activity_place = "Home",
    activity_tag = "Handcraft")

    Activities.objects.create(activities_id = "Boxing",
    activity_desc = "Boxing (French: Boxe) is a sport of fighting with boxing gloves. It has both amateur (also known as Olympic boxing) and professional competitions. The goal of the game is to score more points than the opponent in order to beat the opponent or knock the opponent down to end the game. At the same time, the competitors should try to avoid the opponent's blow.",
    activity_timelength = 60,  # Field name made lowercase.
    activity_photo = "/photos_activities/Boxing.jpg",
    activity_participant = 2,
    activity_place = "Center",
    activity_tag = "Sports")

    Activities.objects.create(activities_id = "Street_workout",
    activity_desc = "Street workout is a form of physical activity that uses parks or public facilities. Originated in Russia, Ukraine and other places, there are now many enthusiast groups around the world, as well as street fitness licenses and competitions.",
    activity_timelength = 90,  # Field name made lowercase.
    activity_photo = "/photos_activities/Street_workout.jpg",
    activity_participant = 1,
    activity_place = "OutDoor",
    activity_tag = "Sports")

    Activities.objects.create(activities_id = "Swimming",
    activity_desc = "Swimming is a skill in which a person floats upward under the action of the buoyancy of the water, and makes the body move regularly in the water through the regular movement of the limbs by means of the buoyancy.",
    activity_timelength = 60,  # Field name made lowercase.
    activity_photo = "/photos_activities/Swimming.jpg",
    activity_participant = 1,
    activity_place = "Center",
    activity_tag = "Sports")

    Activities.objects.create(activities_id = "Fitness",
    activity_desc = "Fitness is a kind of sports, such as various freehand aerobics, rhythmic gymnastics, shape gymnastics and various self-resistance movements, gymnastics, yoga can enhance strength, flexibility, increase endurance, improve coordination, and control the ability of various parts of the body, thereby Make the body strong. If you want to achieve the purpose of reducing stress, exercise at least 3 times a week.",
    activity_timelength = 120,  # Field name made lowercase.
    activity_photo = "/photos_activities/Fitness.jpg",
    activity_participant = 1,
    activity_place = "Center",
    activity_tag = "Sports")

    Activities.objects.create(activities_id = "Badminton",
    activity_desc = "Badminton is an indoor sport that uses a long-handled mesh racket to hit a small ball made of feathers and cork across a net. Badminton matches are played on rectangular courts.",
    activity_timelength = 120,  # Field name made lowercase.
    activity_photo = "/photos_activities/Badminton.jpg",
    activity_participant = 4,
    activity_place = "Outdoor",
    activity_tag = "Sports")

    Activities.objects.create(activities_id = "Shuttlecock",
    activity_desc = "Shuttlecock, also known as Shuttlecock, is a game tool made of chicken feathers inserted on a circular base. As one of the ancient traditional folk sports, shuttlecock originated in the Han Dynasty, and ancient Cuju developed. Popular in the Southern and Northern Dynasties and Sui and Tang Dynasties, it has a history of more than 2,000 years as a simple and easy fitness activity.",
    activity_timelength = 90,  # Field name made lowercase.
    activity_photo = "/photos_activities/Shuttlecock.jpg",
    activity_participant = 3,
    activity_place = "Home",
    activity_tag = "Sports")

    Activities.objects.create(activities_id = "Tennis",
    activity_desc = "Tennis is one of the ball sports. The effective tennis court is a rectangle with a length of 23.77 meters, a width of 8.23 meters for singles and a width of 10.97 meters for doubles. There is a net in the middle, each side of the game occupies one side of the court, and the players hit the ball with a tennis racket.",
    activity_timelength = 180,  # Field name made lowercase.
    activity_photo = "/photos_activities/Tennis.jpg",
    activity_participant = 2,
    activity_place = "Outdoor",
    activity_tag = "Sports")
    Activities.objects.create(activities_id = "LOL",
    activity_desc = "League of Legends (LOL) is a hero-fighting MOBA competitive online game developed by Riot Games and operated by Tencent Games Chinese mainland. The game has hundreds of personality heroes, and has a ranking system, rune system and other features.",
    activity_timelength = 40,  # Field name made lowercase.
    activity_photo = "/photos_activities/LOL.jpg",
    activity_participant = 5,
    activity_place = "Home",
    activity_tag = "Game")

    Activities.objects.create(activities_id = "Flying_Kite",
    activity_desc = "The kite was invented by the working people of ancient China during the Spring and Autumn period of the Eastern Zhou Dynasty, and has been more than 2,000 years old. According to legend, Mo Zhai made a wooden bird from wood and developed it in three years, which is the earliest origin of human kites. Later, Lu Ban used bamboo to improve the kite material of Mo Zhai, until the Eastern Han Dynasty, after Cai Lun improved papermaking, the market began to make kites from paper, called paper kites.",
    activity_timelength = 60,  # Field name made lowercase.
    activity_photo = "/photos_activities/Flying_Kite.jpg",
    activity_participant = 2,
    activity_place = "Outdoor",
    activity_tag = "Game")

    Activities.objects.create(activities_id = "Downfall",
    activity_desc = "In the chilling documentary A Fallen: The Boeing Survey, Oscar-nominated filmmaker Lori Kennedy exposes how corporate disregard and greed led to the crash of two Boeing MAX 737 planes in just five months. Led by aviation experts, journalists, former Boeing employees, the U.S. Congress and victims' families, the film unveils the culture behind a once-admired company that cut costs and hides its eyes.",
    activity_timelength = 90,  # Field name made lowercase.
    activity_photo = "/photos_activities/Downfall.jpg",
    activity_participant = 1,
    activity_place = "Home",
    activity_tag = "Film&TV")

    Activities.objects.create(activities_id = "The_Power_of_the_Dog",
    activity_desc = "The charismatic rancher Phil Burbank (Benedict Cumberbatch) makes those around him both respectful and fearful. When his brother brings home his new wife and her son, Phil torments them in every way until one day he discovers that he also has a glimmer of longing for love.",
    activity_timelength = 110,  # Field name made lowercase.
    activity_photo = "/photos_activities/The_Power_of_the_Dog.jpg",
    activity_participant =1,
    activity_place = "Home",
    activity_tag = "Film&TV")

    Activities.objects.create(activities_id = "Drive_my_Car",
    activity_desc = "Middle-aged stage actor Jia Fu breaks a derailment by his wife Yin, who is a screenwriter, however, he quietly closes the door and quietly leaves, as if nothing had happened, living with his wife harmoniously and lovingly as usual. Until his wife's death, Jiafu failed to be honest with his wife, which became a knot in his heart.",
    activity_timelength = 180,  # Field name made lowercase.
    activity_photo = "/photos_activities/Drive_my_Car.jpg",
    activity_participant =1,
    activity_place = "Home",
    activity_tag = "Film&TV")

    Activities.objects.create(activities_id = "King_Richard",
    activity_desc = "Richard Williams drafted a 78-page plan for his daughters' professional tennis careers, and the girls learned the sport on Compton's dilapidated, overgrown public courts. Before that, their father reportedly got into an argument with some young tough guys who didn't like the sport and wouldn't give up. The Williams sisters went on to become two of the greatest female players in tennis history.",
    activity_timelength = 144,  # Field name made lowercase.
    activity_photo = "/photos_activities/King_Richard.jpg",
    activity_participant =1,
    activity_place = "Home",
    activity_tag = "Film&TV")

    Activities.objects.create(activities_id = "The_Adam_Project",
    activity_desc = "A pilot travels through time and space, confronting the past with his young self and his late father to save the future.",
    activity_timelength = 106,  # Field name made lowercase.
    activity_photo = "/photos_activities/The_Adam_Project.jpg",
    activity_participant =1,
    activity_place = "Home",
    activity_tag = "Film&TV")       

# 验证表单信息 进入首页
def index(request):
    print("views.py.index() called")
    if request.method == "GET":
        status = request.session.get('is_login')
        data_manage = request.session.get("data")
        if not data_manage:
            Activities.objects.all().delete()
            insert_database()
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
            curr_obj = Activities.objects.get(activities_id = image)
            curr_desc = curr_obj.activity_desc
            curr_photo = curr_obj.activity_photo.url
            
        except:
            curr_obj = Activities.objects.get(activities_id = "Hiking")
            image = "Hiking"
            curr_desc = curr_obj.activity_desc
            curr_photo = curr_obj.activity_photo.url

        curr_list = [image,curr_desc,curr_photo]
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
            return render(request,'project.html',{"profile_style" : pro_style, "user_email":user_info.split('@')[0], "reverse_style": rev_style, "user_name" : current_name, "user_photo" : current_photo, 
            "password_opt": password_opt, "projectlist" : curr_list })
        else:
            pro_style = "display:none;"
            rev_style = "display:block;"
            password_opt = "forget password"
            return render(request,'project.html',{"profile_style" : pro_style, "reverse_style": rev_style, 
            "password_opt": password_opt, "projectlist" : curr_list}) 
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
