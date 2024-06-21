"""Методы для отображения и работы с данными блока authentication"""
import http

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def main(request):
    """
    Производит аутентификацию пользователя, или перенаправление на форму регистрации
    @param request: Объект запроса
    @return: Редирект - если произведен вход или требуется регистрация,
     код 404 - если неверные логин/пароль
    """
    if request.method == "POST":
        user = authenticate(username=request.POST["login"], password=request.POST["password"])
        if user:
            login(request, user)
            print("redirecting...")
            return redirect("/")
        return HttpResponse(status=http.HTTPStatus.NOT_FOUND,
                                content="Пользователь с таким логином/паролем не найден!")
    if request.method == "GET":
        return render(request, "auth.html")

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


def registration(request):
    """
    Регистрирует пользователя в системе
    @param request: Объект запроса
    @return: GET - загрузка страницы, POST - обработка формы регистрации
    """
    if request.method == "POST":
        data = request.POST
        user = User.objects.create_user(username=data["username"],
                                        email=data["email"],
                                        password=data["password"],
                                        first_name=data["first-name"],
                                        last_name=data["last-name"])
        user.save()
        return redirect("/auth")
    if request.method == "GET":
        return render(request, "registration.html")

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@login_required
def user_logout(request):
    """
    Производит закрытие пользовательской сессии
    @param request: Объект запроса
    @return:
    """
    logout(request)
    return redirect('/auth')
