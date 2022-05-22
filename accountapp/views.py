from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm


# Create your views here.


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = '로그인에 실패하였습니다'
        else:
            msg = '입력한 양식이 올바르지 않습니다'

    return render(request, "accountapp/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = '회원가입에 성공하였습니다 - 로그인하세요.'
            success = True

            # return redirect("/login/")

        else:
            msg = '양식이 올바르지 않습니다'
    else:
        form = SignUpForm()

    return render(request, "accountapp/register.html", {"form": form, "msg": msg, "success": success})
