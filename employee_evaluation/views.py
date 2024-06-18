from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from self_assessment.models import Employees, SkillsHW, SkillsSW, SkillsPR, Levels


@login_required
def main(request):
    data = {"employees": Employees.objects.values()}
    return render(request, "employee_evaluation.html", data)


@login_required
def about(request):
    levelVals = {}
    for obj in Levels.objects.values():
        levelVals[obj["level"]] = obj["weight"]

    employee = Employees.objects.get(id=request.GET.get("id"))

    hw = SkillsHW.objects.filter(employee_id=employee.id).values_list("product_id", flat=True).distinct()
    sw = SkillsSW.objects.filter(employee_id=employee.id).values_list("product_id", flat=True).distinct()
    pr = SkillsPR.objects.filter(employee_id=employee.id).values_list("process_id", flat=True).distinct()

    hw_data = get_data(SkillsHW, employee, hw, levelVals)
    sw_data = get_data(SkillsSW, employee, sw, levelVals)
    pr_data = []

    # а этот выпендривался и пришлось делать его отдельно
    for process in pr:
        data = SkillsPR.objects.filter(employee_id=employee.id, process_id=process).values_list("level_id", flat=True)
        pr_data.append({"process": process, "level": data[0]})

    data = {"hw_data": hw_data, "hw_max_score": 48, "sw_data": sw_data, "sw_max_score": 20, "pr_data": pr_data}

    print(data["pr_data"])
    return render(request, "employee_evaluation_about.html", data)


def get_data(DBObject, employee, product_list, levelVals):
    arr = []
    for product in product_list:
        data = DBObject.objects.filter(employee_id=employee.id, product_id=product).values_list("task_id", "level_id")
        tasks = []
        score = 0
        for i in data:
            tasks.append((i[0], i[1]))
            score += levelVals[i[1]]
        arr.append({"product": product, "tasks": tasks, "score": score})

    return arr
