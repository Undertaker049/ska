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


def upload_assessment(request):
    print(request.POST)
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
