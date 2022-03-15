from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.conf import settings
from .forms import LoginForm

import os
import time

# Create your views here.


def do_register(request):
    try:
        msg = ""
        if request.method == "GET":
            return render(request, "register.html", locals())
        if request.method == "POST":
            user = request.user
            datas = request.POST
            username = request.POST.get("username")
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            print(username)
            print(password)
            print(password2)

            if len(username) < 6 or len(password) < 6 or len(password2) < 6:
                msg="账号密码必须大于6位"
                return render(request, "register.html", locals())
            if password != password2:
                msg="两次输入的密码不一致"
                return render(request, "register.html", locals())
            if "@" not in username:
                msg = "邮箱格式不正确！"
                return render(request, "register.html", locals())
            only = UserProfile.objects.filter(username=username)
            if len(only) > 0:
                msg = "邮箱已经存在"
                return render(request, "register.html", locals())
            new_user = UserProfile()
            new_user.username = username
            new_user.email = username
            new_user.set_password(password)
            new_user.mpassword = password
            new_user.save()
            return redirect("accounts:login")
        else:
            return render(request, "register.html", locals())
    except Exception as e:
        print(e)
        msg = "添加失败系统错误"
        return render(request, "register.html", locals())


def user_login(request):
    try:
        if request.user.is_authenticated:
            return redirect("/")
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(request, user)
                else:
                    errorinfo = "账号或密码不正确"
                    return render(request, 'login.html', {'login_form': login_form, "errorinfo":errorinfo})
                return redirect("/")
            else:
                errorinfo = "账号或密码不正确或格式错误"
                return render(request, 'login.html', {'login_form': login_form, "errorinfo":errorinfo})
        else:
            login_form = LoginForm()
            return render(request, 'login.html', {'login_form': login_form})
    except Exception as e:
        login_form = LoginForm()
        print(e)
        errorinfo = "系统错误"
        return render(request, 'login.html', {'login_form': login_form, "errorinfo":errorinfo})

@login_required
def user_logout(request):
    try:
        logout(request)
        return redirect('accounts:login')
    except Exception as e:
        print(e)
    return render(request, "error.html", {"msg":"退出错误"})


@login_required
def my_info(request):
    try:
        user = request.user
        if request.method == "GET":
            return render(request, "my_info.html", locals())
        if request.method == "POST":
            username = request.POST.get("username", "")
            mobile = request.POST.get("mobile", "")
            sex = request.POST.get("sex", "")
            avatar = request.FILES.get('avatar')
            print(username)
            print(mobile)
            print(sex)
            print(avatar)
            if username == "" or username == None or len(username) < 6:
                msg = "用户名不能为空，必须大于6位"
                return render(request, "my_info.html", locals())
            if mobile == "" or mobile == None or len(mobile) != 11:
                msg = "手机号不能为空，必须11位且格式正确"
                return render(request, "my_info.html", locals())
            if avatar != None:
                stamp = str((int(round(time.time() * 1000))))
                imgname = stamp + avatar.name
                print(imgname)
                path = os.path.join(settings.MEDIA_ROOT, 'avatar', imgname)
                print(path)
                url = "avatar/" + imgname
                print(url)
                with open(path, 'wb') as f:
                    for chunk in avatar.chunks():
                        f.write(chunk)
            user.username = username
            user.mobile = mobile
            user.sex = sex
            if avatar != None:
                user.avatar = url
            user.save()
            msg = "修改成功"
            return render(request, "my_info.html", locals())
    except Exception as e:
        print(e)
        msg = "系统错误"
        return render(request, "my_info.html", locals())


@login_required
def modify(request):
    try:
        user = request.user
        if request.method == 'POST':
            oldpassword = request.POST.get("oldpassword")
            newpassword = request.POST.get("newpassword")
            conpassword = request.POST.get("conpassword")
            print(user.mpassword)
            print(oldpassword)
            if user.mpassword != oldpassword:
                errorinfo = "旧密码错误"
                return render(request, 'modify.html',  locals())
            if newpassword != conpassword:
                errorinfo = "新旧密码不一致"
                return render(request, 'modify.html',  locals())
            if len(newpassword) < 6:
                errorinfo = "密码大于6位"
                return render(request, 'modify.html', locals())
            user.mpassword = newpassword
            user.set_password(newpassword)
            user.save()
            logout(request)
            return redirect("/accounts/login")
        else:
            return render(request, 'modify.html', locals())
    except Exception as e:
        print(e)
        errorinfo = "系统错误"
        return render(request, 'modify.html',  locals())
