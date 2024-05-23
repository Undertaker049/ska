import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .models import *


@login_required
def main(request):
    hw = Hardware.objects.values_list('product', flat=True).distinct()
    hw_disciplines = TaskHW.objects.values_list('task', flat=True).distinct()

    sw = Software.objects.values_list('product', flat=True).distinct()
    sw_disciplines = TaskSW.objects.values_list('task', flat=True).distinct()

    skills = Processes.objects.values_list('process', flat=True).distinct()
    skills_disciplines = ['level']

    levels = Levels.objects.values_list('weight', 'level').distinct()

    hw_page = {"id": "HW",
               "subpages": "hw-element",
               "tech": hw,
               "disciplines": hw_disciplines,
               "subpages_radio": "hw-radio",
               "button": "hw-button"}
    sw_page = {"id": "SW",
               "subpages": "sw-element",
               "tech": sw,
               "disciplines": sw_disciplines,
               "subpages_radio": "sw-radio",
               "button": "sw-button"}
    skills_page = {"id": "Skills",
                   "subpages": "skills-element",
                   "tech": skills,
                   "disciplines": skills_disciplines,
                   "subpages_radio": "skills-radio",
                   "button": "skills-button"}

    data = {"pages": [hw_page, sw_page, skills_page],
            "levels": levels}
    # return render(request, 'self_assessment.html', data)
    response = render(request, 'testPage.html', data)
    response.set_cookie("user", request.user.email, expires=request.session.get_expiry_date())
    return response


@login_required
def validate_name(request):
    employee = Employees.objects.filter(name=request.GET.get("name")).first()
    if employee is not None:
        if SkillsHW.objects.filter(employee_id=employee.id).exists() | SkillsSW.objects.filter(
                employee_id=employee.id).exists() | SKillsPr.objects.filter(employee_id=employee.id).exists():
            return HttpResponse("Ваши данные уже есть в базе", status=403)
    else:
        return HttpResponse("Работник не найден", status=404)

    return HttpResponse(status=200)


@login_required
def upload_assessment(request):
    data = json.loads(request.POST.get("form"))
    user_id = Employees.objects.filter(name=data.get("name")).values_list('id', flat=True).first()

    hw_tasks = TaskHW.objects.values_list("task", flat=True).distinct()
    for product in data.get("HW"):
        product_name = product.get("_product").replace('\'', "")
        hw_tasks_levels = product.get("_selections")
        for i in range(len(hw_tasks)):
            obj = SkillsHW(employee_id=user_id,
                           product=Hardware.objects.get(product=product_name),
                           task=TaskHW.objects.get(task=hw_tasks[i]),
                           level=Levels.objects.get(weight=hw_tasks_levels[i]))
            obj.save()

    sw_tasks = TaskSW.objects.values_list("task", flat=True).distinct()
    for product in data.get("SW"):
        product_name = product.get("_product").replace('\'', "")
        sw_tasks_levels = product.get("_selections")
        for i in range(len(sw_tasks)):
            obj = SkillsSW(employee_id=user_id,
                           product=Software.objects.get(product=product_name),
                           task=TaskSW.objects.get(task=sw_tasks[i]),
                           level=Levels.objects.get(weight=sw_tasks_levels[i]))
            obj.save()

    for product in data.get("Processes"):
        print(product)
        process_name = product.get("_product").replace('\'', "")
        processes_tasks_level = product.get("_selections")[0]
        obj = SKillsPr(employee_id=user_id,
                       process=Processes.objects.get(process=process_name),
                       level=Levels.objects.get(weight=processes_tasks_level))
        obj.save()

    return HttpResponse(status=200)
