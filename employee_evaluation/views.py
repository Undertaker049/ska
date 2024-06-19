from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

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

    hw, sw, pr = get_products(employee)

    hw_data = get_products_scores(SkillsHW, employee, hw, levelVals)
    sw_data = get_products_scores(SkillsSW, employee, sw, levelVals)
    pr_data = get_products_scores(SkillsPR, employee, pr, levelVals, False)

    data = {"hw_data": hw_data, "hw_max_score": 48, "sw_data": sw_data, "sw_max_score": 20, "pr_data": pr_data}
    return render(request, "employee_evaluation_about.html", data)


def about_block(request):
    employee = Employees.objects.get(id=request.GET.get("id"))

    data = ""
    match request.GET.get("block"):
        case "hw":
            hw_data = get_products_tasks_levels(SkillsHW, employee, get_products(employee, "hw"))
            print(hw_data)
            data = render_to_string("employee-evaluation-about-block.html", {"data": hw_data, "long": True})
        case "sw":
            sw_data = get_products_tasks_levels(SkillsHW, employee, get_products(employee, "sw"))
            data = render_to_string("employee-evaluation-about-block.html", {"data": sw_data, "long": True})
        case "pr":
            pr_data = get_products_tasks_levels(SkillsHW, employee, get_products(employee, "pr"), False)
            data = render_to_string("employee-evaluation-about-block.html", {"data": pr_data, "long": False})
    print(data)
    return JsonResponse({"data": data})


def get_products(employee, key="all"):
    if key == "all":
        return (SkillsHW.objects.filter(employee_id=employee.id).values_list("product_id", flat=True).distinct(),
                SkillsSW.objects.filter(employee_id=employee.id).values_list("product_id", flat=True).distinct(),
                SkillsPR.objects.filter(employee_id=employee.id).values_list("process_id", flat=True).distinct())
    elif key == "hw":
        return SkillsHW.objects.filter(employee_id=employee.id).values_list("product_id", flat=True).distinct()
    elif key == "sw":
        return SkillsSW.objects.filter(employee_id=employee.id).values_list("product_id", flat=True).distinct()
    elif key == "pr":
        return SkillsPR.objects.filter(employee_id=employee.id).values_list("process_id", flat=True).distinct()


def get_products_scores(DBObject, employee, product_list, levelVals, is_long=True):
    arr = []
    if is_long:
        for product in product_list:
            data = DBObject.objects.filter(employee_id=employee.id, product_id=product).values_list("level_id",
                                                                                                    flat=True)
            score = 0
            for i in data:
                score += levelVals[i]
            arr.append({"product": product, "score": score})
        return arr
    else:
        for process in product_list:
            data = SkillsPR.objects.filter(employee_id=employee.id, process_id=process).values_list("level_id",
                                                                                                    flat=True)
            arr.append({"process": process, "level": data[0]})
        return arr


def get_products_tasks_levels(DBObject, employee, product_list, is_long=True):
    arr = []
    if is_long:
        for product in product_list:
            data = DBObject.objects.filter(employee_id=employee.id, product_id=product).values_list("task_id",
                                                                                                    "level_id")
            tasks = []
            for i in data:
                tasks.append((i[0], i[1]))
            arr.append({"product": product, "tasks": tasks})
        return arr
    else:
        for process in product_list:
            data = SkillsPR.objects.filter(employee_id=employee.id, process_id=process).values_list("level_id",
                                                                                                    flat=True)
            arr.append({"process": process, "level": data[0]})
        return arr
