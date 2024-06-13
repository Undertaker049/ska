import http

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def main(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["login"], password=request.POST["password"])
        if user:
            login(request, user)
            return redirect("/")
        else:
            return HttpResponse(status=http.HTTPStatus.NOT_FOUND, content="Пользователь с таким логином/паролем не найден!")
    elif request.method == "GET":
        return render(request, "auth.html")


def registration(request):
    if request.method == "POST":
        data = request.POST
        user = User.objects.create_user(username=data["username"],
                                        email=data["email"],
                                        password=data["password"],
                                        first_name=data["first-name"],
                                        last_name=data["last-name"])
        user.save()
        return redirect("/auth")
    elif request.method == "GET":
        return render(request, "registration.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')
