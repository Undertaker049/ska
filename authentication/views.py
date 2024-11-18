"""Методы для отображения и работы с данными блока authentication"""
import http

from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from self_assessment.models import Employees, Department


def main(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["login"], password=request.POST["password"])

        if user:
            login(request, user)
            return redirect("/")

        return HttpResponse(status=http.HTTPStatus.NOT_FOUND,
                          content="Пользователь с таким логином/паролем не найден")

    if request.method == "GET":
        return render(request, "auth.html")

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


def registration(request):
    departments = [
        {'id': 'integration', 'name': 'Отдел системной интеграции', 'icon': 'bi-building'},
        {'id': 'service', 'name': 'Сервисный центр', 'icon': 'bi-tools'},
        {'id': 'project', 'name': 'Проектный отдел', 'icon': 'bi-kanban'},
        {'id': 'sales', 'name': 'Отдел продаж', 'icon': 'bi-cart'}
    ]

    if request.method == "POST":
        try:
            data = request.POST

            if User.objects.filter(username=data["username"]).exists():
                return HttpResponse(
                    status=http.HTTPStatus.BAD_REQUEST,
                    content="Пользователь с таким именем уже существует!"
                )

            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                first_name=data["first-name"],
                last_name=data["last-name"]
            )
            user.save()

            department = Department.objects.get_or_create(
                name=get_department_name(data['department'])
            )[0]

            employee = Employees.objects.create(
                name=f"{data['first-name']} {data['last-name']}",
                department=department
            )
            employee.save()

            return HttpResponse(status=http.HTTPStatus.OK)

        except IntegrityError as e:
            return HttpResponse(
                status=http.HTTPStatus.BAD_REQUEST,
                content="Ошибка при создании пользователя: возможно, такой пользователь уже существует"
            )

        except Exception as e:
            return HttpResponse(
                status=http.HTTPStatus.INTERNAL_SERVER_ERROR,
                content=f"Произошла ошибка при регистрации: {str(e)}"
            )

    if request.method == "GET":
        return render(request, "registration.html", {'departments': departments})

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


def get_department_name(department_code):
    departments = {
        'integration': 'Отдел системной интеграции',
        'service': 'Сервисный центр',
        'project': 'Проектный отдел',
        'sales': 'Отдел продаж'
    }

    return departments.get(department_code)


@login_required
def user_logout(request):
    """
    Производит закрытие пользовательской сессии
    :param request: Объект запроса
    :return: редирект на страницу входа
    """
    logout(request)
    return redirect('/auth')