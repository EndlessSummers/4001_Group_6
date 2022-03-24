from django.shortcuts import render,HttpResponse,redirect
import pymysql

# Create your views here.
#登录页面
def login(request):
    #指定要访问的页面，render的功能：讲请求的页面结果提交给客户端
    return render(request,'login.html')

def input_email(request):

    return render(request,'input_email.html')

def reg_email(request):
   
    return render(request,'reg_email.html')

def reg_form(request):
    return render(request, 'reg_form.html')

def user_page(request):
    return render(request, 'userpage.html')

def change_pswd(request):
    return render(request, 'input_changepassword.html')

def new_pswd(request):
    return render(request, 'input_newpassword.html')

def cancel_check(request):
    return render(request, 'input_cancelcheck.html')

def pass_email(request):
    return render (request, 'pass_email.html')

def email(request):
    return render (request, 'email.html')

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