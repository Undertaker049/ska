"""Методы для отображения и работы с данными блока self_assessment"""
import http
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .models import (Hardware,
                     TaskHW,
                     SkillsHW,
                     Software,
                     TaskSW,
                     SkillsSW,
                     Processes,
                     SkillsPR,
                     Levels,
                     Employees)

def get_products_data():
    return {
        'hw_products': Hardware.objects.values_list('product', flat=True),
        'sw_products': Software.objects.values_list('product', flat=True),
        'hw_tasks': TaskHW.objects.values_list('task', flat=True),
        'sw_tasks': TaskSW.objects.values_list('task', flat=True),
        'processes': Processes.objects.values_list('process', flat=True)
    }

def get_levels():
    return Levels.objects.order_by("weight").values_list('level', flat=True)

@login_required
def main(request):
    """
    Метод выводит опросник по заданным дисциплинам, дисциплины берутся из БД
    :param request: Объект запроса
    :return: рендер страницы
    """
    if request.method != "GET":
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    products_data = get_products_data()

    data = {
        "blocks": {
            "hw": {
                "name": "Hardware",
                "products": products_data['hw_products'],
                "tasks": products_data['hw_tasks']
            },
            "sw": {
                "name": "Software",
                "products": products_data['sw_products'],
                "tasks": products_data['sw_tasks']
            },
            "pr": {
                "name": "Processes",
                "products": products_data['processes'],
            },
        },
        "levels": get_levels()
    }

    return render(request, "self_assessment.html", context={"data": data})

@login_required
def old(request):
    """
    Старый метод выводит опросник по заданным дисциплинам, дисциплины берутся из БД
    :param request: Объект запроса
    :return: рендер страницы
    """
    if request.method != "GET":
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    hw = Hardware.objects.values_list('product', flat=True).distinct()
    hw_disciplines = TaskHW.objects.values_list('task', flat=True).distinct()

    sw = Software.objects.values_list('product', flat=True).distinct()
    sw_disciplines = TaskSW.objects.values_list('task', flat=True).distinct()

    skills = Processes.objects.values_list('process', flat=True).distinct()
    skills_disciplines = ['level']

    levels = Levels.objects.values_list('weight', 'level').distinct()

    # Id - id html-блока,
    # subpages - название класса html-блоков для конкретных процессов/технологий etc.,
    # tech - конкретная технология/процесс etc., по которой есть вопросы,
    # disciplines - Вопросы по конкретной технологии/процессу etc.,
    # long-list - Пока я не придумал как нормально переписать форму - костыль,
    # чтобы убрать генерацию кнопок перехода
    # к следующему блоку на страницах, где блоки вопросов короткие(как Processes например)
    hw_page = {"id": "HW",
               "name": "Hardware",
               "subpages": "hw-element",
               "tech": hw,
               "disciplines": hw_disciplines,
               "longList": True
               }
    sw_page = {"id": "SW",
               "name": "Software",
               "subpages": "sw-element",
               "tech": sw,
               "disciplines": sw_disciplines,
               "longList": True
               }
    skills_page = {"id": "Processes",
                   "name": "Processes",
                   "subpages": "processes-element",
                   "tech": skills,
                   "disciplines": skills_disciplines,
                   "longList": False
                   }

    data = {"pages": [hw_page, sw_page, skills_page],
            "levels": levels}
    return render(request, 'self_assessment_old.html', data)


@login_required
def validate_name(request):
    """
    Проверка на наличие работника с такими Фамилией и Именем в БД
    :param request: Объект запроса
    :return: код 200 - если найден, 404 - если не найден
    """
    if request.method != "GET":
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    employee = (Employees.
                objects.
                filter(name=f'{request.user.first_name} {request.user.last_name}').
                get())
    print(f'{request.user.first_name} {request.user.last_name}')
    if employee is not None:
        if (SkillsHW.objects.filter(employee_id=employee.id).exists() |
                SkillsSW.objects.filter(employee_id=employee.id).exists() |
                SkillsPR.objects.filter(employee_id=employee.id).exists()):
            return HttpResponse("Ваши данные уже есть в базе", status=http.HTTPStatus.FORBIDDEN)
    else:
        return HttpResponse("Работник не найден", status=http.HTTPStatus.NOT_FOUND)

    return HttpResponse(status=http.HTTPStatus.OK)


@login_required
def upload_assessment(request) -> HttpResponse:
    """
    Метод обрабатывает результаты заполненной формы и вносит их в БД
    :param request: Объект запроса
    :return: Код 200 - если все результаты были успешно записаны в БД
    """
    if request.method != "POST":
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    print(request.POST)
    data = json.loads(request.POST.get("data"))

    user_id = (Employees.
               objects.
               filter(name=f'{request.user.first_name} {request.user.last_name}').
               values_list('id', flat=True).
               first())

    hw = dict(data["HW"])
    for item in hw.items():
        discipline = item[0].split(":")
        obj = SkillsHW(employee_id=user_id,
                       product=Hardware.objects.get(product=discipline[0]),
                       task=TaskHW.objects.get(task=discipline[1]),
                       level=Levels.objects.get(level=item[1])
                       )
        print(obj.level)

    sw = dict(data["SW"])
    for item in sw.items():
        discipline = item[0].split(":")
        obj = SkillsSW(employee_id=user_id,
                       product=Software.objects.get(product=discipline[0]),
                       task=TaskSW.objects.get(task=discipline[1]),
                       level=Levels.objects.get(level=item[1])
                       )
        # obj.save()
        print(obj.level)

    pr = dict

    return HttpResponse(status=http.HTTPStatus.OK)
