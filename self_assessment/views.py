"""Методы для отображения и работы с данными блока self_assessment"""
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


@login_required
def main(request):
    """
    Метод выводит опросник по заданным дисциплинам, дисциплины берутся и БД
    @param request: Объект запроса
    @return: django.shortcuts.render
    """
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
               "subpages": "hw-element",
               "tech": hw,
               "disciplines": hw_disciplines,
               "longList": True
               }
    sw_page = {"id": "SW",
               "subpages": "sw-element",
               "tech": sw,
               "disciplines": sw_disciplines,
               "longList": True
               }
    skills_page = {"id": "Processes",
                   "subpages": "processes-element",
                   "tech": skills,
                   "disciplines": skills_disciplines,
                   "longList": False
                   }

    data = {"pages": [hw_page, sw_page, skills_page],
            "levels": levels}
    return render(request, 'self_assessment.html', data)


@login_required
def validate_name(request):
    """
    Проверка на наличие работника с такими Фамилией и Именем в БД
    @param request: Объект запроса
    @return: код 200 - если найден, 404 - если не найден
    """
    employee = (Employees.
                objects.
                filter(name=f'{request.user.first_name} {request.user.last_name}').
                first())
    if employee is not None:
        if (SkillsHW.objects.filter(employee_id=employee.id).exists() |
                SkillsSW.objects.filter(employee_id=employee.id).exists() |
                SkillsPR.objects.filter(employee_id=employee.id).exists()):
            return HttpResponse("Ваши данные уже есть в базе", status=403)
    else:
        return HttpResponse("Работник не найден", status=404)

    return HttpResponse(status=200)


@login_required
def upload_assessment(request) -> HttpResponse:
    """
    Метод обрабатывает результаты заполненной формы и вносит их в БД
    @param request: Объект запроса
    @return: Код 200 - если все результаты были успешно записаны в БД
    """
    data = json.loads(request.POST.get("form"))
    user_id = (Employees.
               objects.
               filter(name=f'{request.user.first_name} {request.user.last_name}').
               values_list('id', flat=True).
               first())

    hw_tasks = TaskHW.objects.values_list("task", flat=True).distinct()
    for product in data.get("HW"):
        product_name = product.get("_product").replace('\'', "")
        hw_tasks_levels = product.get("_selections")
        for i, hw_task in enumerate(hw_tasks):
            obj = SkillsHW(employee_id=user_id,
                           product=Hardware.objects.get(product=product_name),
                           task=TaskHW.objects.get(task=hw_task),
                           level=Levels.objects.get(weight=hw_tasks_levels[i]))
            obj.save()

    sw_tasks = TaskSW.objects.values_list("task", flat=True).distinct()
    for product in data.get("SW"):
        product_name = product.get("_product").replace('\'', "")
        sw_tasks_levels = product.get("_selections")
        for i, sw_task in enumerate(sw_tasks):
            obj = SkillsSW(employee_id=user_id,
                           product=Software.objects.get(product=product_name),
                           task=TaskSW.objects.get(task=sw_task),
                           level=Levels.objects.get(weight=sw_tasks_levels[i]))
            obj.save()

    for product in data.get("Processes"):
        process_name = product.get("_product").replace('\'', "")
        processes_tasks_level = product.get("_selections")[0]
        obj = SkillsPR(employee_id=user_id,
                       process=Processes.objects.get(process=process_name),
                       level=Levels.objects.get(weight=processes_tasks_level))
        obj.save()

    return HttpResponse(status=200)
