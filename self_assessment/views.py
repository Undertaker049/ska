import json

from django.http import HttpResponse
from django.shortcuts import render

from .forms import MainForm
from .models import *


def main(request):
    hw = Hardware.objects.values_list('product', flat=True).distinct()
    hw_disciplines = TaskHW.objects.values_list('task', flat=True).distinct()

    sw = Software.objects.values_list('product', flat=True).distinct()
    sw_disciplines = TaskSW.objects.values_list('task', flat=True).distinct()

    skills = Processes.objects.values_list('process', flat=True).distinct()
    skills_disciplines = ['level']

    levels = Levels.objects.values_list('weight', 'level').distinct()

    hw_page = {"id": "HW", "subpages": "hw-element", "tech": hw, "disciplines": hw_disciplines}
    sw_page = {"id": "SW", "subpages": "sw-element", "tech": sw, "disciplines": sw_disciplines}
    skills_page = {"id": "Skills", "subpages": "skills-element", "tech": skills, "disciplines": skills_disciplines}

    data = {"pages": [hw_page, sw_page, skills_page],
            "levels": levels}
    return render(request, 'self_assessment.html', data)


def validate_name(request):
    if Employees.objects.filter(name=request.GET.get("name")).exists():
        return HttpResponse(status=200)
    else:
        return HttpResponse("Работник не найден", status=404)


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


def test(request):
    hw_products = Hardware.objects.values_list('product', flat=True).distinct()
    hw_tasks = []
    for task in TaskHW.objects.values_list('task', flat=True).distinct():
        hw_tasks.append(MainForm(label=task, _class="hw-element"))

    sw_products = Software.objects.values_list('product', flat=True).distinct()
    sw_tasks = []
    for task in TaskHW.objects.values_list('task', flat=True).distinct():
        sw_tasks.append(MainForm(label=task, _class="sw-element"))

    processes = Processes.objects.values_list('process', flat=True).distinct()
    processes_tasks = [MainForm(label="Level", _class="processes-element")]

    hw_page = {"id": "HW", "products": hw_products, "tasks": hw_tasks}
    sw_page = {"id": "SW", "products": sw_products, "tasks": sw_tasks}
    processes_page = {"id": "Processes", "products": processes, "tasks": processes_tasks}

    pages = [hw_page, sw_page, processes_page]

    return render(request, 'testPage.html', {"pages": pages})
