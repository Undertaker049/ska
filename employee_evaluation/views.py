"""Методы для отображения и работы с данными блока employee evaluation"""
import http
import json
from array import array

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from certificate.models import CertificateSubCategory, CertificateCategory
from .models import Reviews
from self_assessment.models import Employees, SkillsHW, SkillsSW, SkillsPR, Levels, Hardware, TaskHW, Software, TaskSW, \
    Processes

HW_MAX_SCORE = 48
SW_MAX_SCORE = 20

level_vals = {}
for o in Levels.objects.values():
    level_vals[o["level"]] = o["weight"]


@login_required
def main(request):
    """
    Выводит список сотрудников в виде таблицы

    :param request: Объект запроса
    :return: GET - загружает страницу со списком сотрудников
    """
    if request.method == "GET":
        employee = Employees.objects.get(name=f"{request.user.first_name} {request.user.last_name}")
        data = {"employees": Employees.objects.values(),
                "is_supervisor": employee.is_supervisor}
        if employee.is_supervisor:
            data["hw"] = Hardware.objects.values_list('product', flat=True)
            data["hw_tasks"] = TaskHW.objects.values_list('task', flat=True)
            data["sw"] = Software.objects.values_list('product', flat=True)
            data["sw_tasks"] = TaskSW.objects.values_list('task', flat=True)
            data["processes"] = Processes.objects.values_list('process', flat=True)
            data["certificate_category"] = CertificateCategory.objects.values_list('category', flat=True)
            data["certificate_subcategory"] = []
            for obj in CertificateSubCategory.objects.values_list('subcategory', 'subcategory_of'):
                data["certificate_subcategory"].append(obj)
            data["hw_max"] = HW_MAX_SCORE
            data["sw_msx"] = SW_MAX_SCORE
            data["levels"] = Levels.objects.order_by("weight").values_list('level', flat=True)

        return render(request, "employee_evaluation.html", data)

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@login_required
def about(request):
    """
    Выводит информацию о навыках сотрудника на основе данных формы из self assessment

    :param request: Объект запроса
    :return: GET - Загружает страницу с навыками сотрудника
    """
    if request.method == "GET":
        employee = Employees.objects.get(id=request.GET.get("id"))

        hw, sw, pr = get_products(employee)

        hw_data = get_products_scores(SkillsHW, employee, hw)
        sw_data = get_products_scores(SkillsSW, employee, sw)
        pr_data = get_products_scores(SkillsPR, employee, pr, False)

        data = {"hw_data": hw_data,
                "hw_max_score": HW_MAX_SCORE,
                "sw_data": sw_data,
                "sw_max_score": SW_MAX_SCORE,
                "pr_data": pr_data}
        return render(request, "employee_evaluation_about.html", data)

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@login_required
def about_block(request):
    """
    Выводит подробную информацию об уровнях компетенций определенного блока

    :param request: Объект запроса
    :return: GET - Загружает страницу с информацией об уровнях компетенций
    """
    if request.method == "GET":
        employee = Employees.objects.get(id=request.GET.get("id"))

        data = {}
        match request.GET.get("block"):
            case "hw":
                hw_data = get_products_tasks_levels(SkillsHW,
                                                    employee,
                                                    get_products(employee, "hw"))
                data = {"data": hw_data, "long": True}
            case "sw":
                sw_data = get_products_tasks_levels(SkillsSW,
                                                    employee,
                                                    get_products(employee, "sw"))
                data = {"data": sw_data, "long": True}
            case "pr":
                pr_data = get_products_tasks_levels(SkillsPR,
                                                    employee,
                                                    get_products(employee, "pr"), False)
                data = {"data": pr_data, "long": False}
        return render(request, "employee_evaluation_about_block.html", data)

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@login_required
def reviews(request):
    """
    Выводит список полученных и отправленных ревью

    :param request: Объект запроса
    :return: Рендер страницы с ревью | method_not_allowed если запрос не GET
    """
    if request.method == "GET":
        employee = (Employees.
                    objects.
                    filter(name=f'{request.user.first_name} {request.user.last_name}').
                    values().
                    first())

        revs = Reviews.objects.filter(Q(reviewer_id=employee["id"]) | Q(reviewed_id=employee["id"])).values()
        return render(request, "employee_evaluation_reviews.html", {"revs": revs})

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@login_required
def review(request):
    if request.method == "GET":
        return JsonResponse({"data": Reviews.objects.filter(id=request.GET["id"]).values().first()["message"]})
    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@login_required
def delete_review(request, review_id):
    if request.method == "DELETE":
        obj = Reviews.objects.get(id=review_id)
        employee_id = Employees.objects.get(name=f"{request.user.first_name} {request.user.last_name}").id
        if obj.reviewer_id == employee_id:
            obj.delete()
            return HttpResponse(status=http.HTTPStatus.OK)
        else:
            return HttpResponse(status=http.HTTPStatus.FORBIDDEN, content="Нельзя удалить чужое ревью!")
    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@login_required
def upload_review(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        employee = (Employees.
                    objects.
                    filter(name=f'{request.user.first_name} {request.user.last_name}').
                    values().
                    first())

        data = request.POST

        if employee["id"] == data["rev_id"]:
            return HttpResponse(status=http.HTTPStatus.FORBIDDEN, content="Нельзя писать отзыв себе же")

        obj = Reviews(reviewer_id=employee["id"],
                      reviewed_id=data["rev_id"],
                      block=data["block"],
                      message=data["message"],
                      theme=data["theme"])
        try:
            obj.save()
            return HttpResponse(status=200)
        except Exception as e:
            # TODO переделать в логгер
            print(e)
            return HttpResponse(status=http.HTTPStatus.INTERNAL_SERVER_ERROR, content="Не удалось сохранить запись")

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@login_required
def get_subordinates(request):
    employee = Employees.objects.get(name=f"{request.user.first_name} {request.user.last_name}")
    return JsonResponse(
        {"data": list(Employees.objects.filter(subordinate_of=employee.id).values_list('id', flat=True))})


@login_required
def subordinates_apply_filters(request):
    if request.method == "POST":
        data = json.loads(request.POST.get("data"))
        filters = data["filters"]
        subordinates = Employees.objects.filter(id__in=data["subordinates"]).values()
        for _id in filters:
            _filter = filters[_id]
            if (_filter["block"] == "hw") | (filters[_id]["block"] == "sw"):
                if _filter["task"] != "Total":
                    for subordinate in subordinates:
                        if _filter["block"] == "hw":
                            obj = SkillsHW.objects.filter(employee_id=subordinate["id"],
                                                          product=_filter["product"],
                                                          task=_filter["task"]).get()
                        else:
                            obj = SkillsSW.objects.filter(employee_id=subordinate["id"],
                                                          product=_filter["product"],
                                                          task=_filter["task"]).get()
                        # мне больно на это смотреть (; _ ;)
                        print(f"USR: {level_vals[obj.level_id]} REQ: {level_vals[_filter['value']]}")
                        if _filter["sign"] == ">":
                            if level_vals[obj.level_id] > level_vals[_filter["value"]]:
                                print(level_vals[obj.level_id] > level_vals[_filter["value"]])
                                continue
                        elif _filter["sign"] == "<":
                            if level_vals[obj.level_id] < level_vals[_filter["value"]]:
                                print(level_vals[obj.level_id] < level_vals[_filter["value"]])
                                continue
                        elif _filter["sign"] == "=":
                            if level_vals[obj.level_id] == level_vals[_filter["value"]]:
                                print(level_vals[obj.level_id] == level_vals[_filter["value"]])
                                continue

                        print("удаляю по не тотал")
                        subordinates = subordinates.exclude(id=subordinate["id"])
                elif _filter["task"] == "Total":
                    for subordinate in subordinates:
                        score = get_product_score(SkillsHW if _filter["block"] == "hw" else SkillsSW,
                                                  subordinate["id"],
                                                  _filter["product"])

                        if _filter["sign"] == ">":
                            if score > int(_filter["value"]):
                                print(f"Требуемое {int(_filter['value'])} < Текущее {score}")
                                continue
                        elif _filter["sign"] == "<":
                            if score < int(_filter["value"]):
                                print(f"Требуемое {int(_filter['value'])} > Текущее {score}")
                                continue
                        elif _filter["sign"] == "=":
                            if score == int(_filter["value"]):
                                print(f"Требуемое {int(_filter['value'])} == Текущее {score}")
                                continue

                        print("удаляю по тотал")
                        subordinates = subordinates.exclude(id=subordinate["id"])

            elif _filter["block"] == "pr":
                print(filters[_id])
            elif _filter["block"] == "cr":
                print(filters[_id])

            print(len(subordinates))
            if len(subordinates) == 0:
                print("Отправляю сообщение об ошибке")
                return HttpResponse(status=http.HTTPStatus.INTERNAL_SERVER_ERROR,
                                    content=_id)

        return HttpResponse(status=http.HTTPStatus.OK, content="Вcё гуд")
    else:
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


def get_products(employee: Employees, key="all"):
    """
    Возвращает список продуктов или процессов из базы данных

    :param employee: Объект БД, представляющий работника
    :param key: Ключ, ["all","hw","sw","pr"], в зависимости от него возвращаются продукты или процессы разных блоков
    :return: Массив(ы) строк
    """
    if key == "all":
        return (SkillsHW.
                objects.
                filter(employee_id=employee.id).values_list("product_id", flat=True).
                distinct(),
                SkillsSW.
                objects.
                filter(employee_id=employee.id).values_list("product_id", flat=True).
                distinct(),
                SkillsPR.
                objects.
                filter(employee_id=employee.id).values_list("process_id", flat=True).
                distinct())
    if key == "hw":
        return (SkillsHW.
                objects.
                filter(employee_id=employee.id).values_list("product_id", flat=True).
                distinct())
    if key == "sw":
        return (SkillsSW.
                objects.
                filter(employee_id=employee.id).values_list("product_id", flat=True).
                distinct())
    if key == "pr":
        return (SkillsPR.
                objects.
                filter(employee_id=employee.id).values_list("process_id", flat=True).
                distinct())

    return None


def get_products_scores(db_object: type[SkillsHW | SkillsSW | SkillsPR],
                        employee: Employees,
                        product_list: array,
                        is_long=True):
    """
    Возвращает массив словарей, где 1 словарь - 1 продукт или процесс и его суммарный уровень

    :param db_object: Объект БД, представляющий таблицу с компетенциями сотрудников по блоку
    :param employee: Объект БД, представляющий работника
    :param product_list: Список продуктов или процессов, для которых нужно собрать информацию
    :param is_long: Ключ, определяющий по какому шаблону будет составлен итоговый массив.
        True - у каждой дисциплины есть суб-дисциплины, а у них уже уровни.
        False - у дисциплины есть только ее собственный уровень.
    :return: Массив словарей формата [{"product", "score"}, ...] | [{"process", "level"}, ...]
    """
    arr = []
    if is_long:
        for product in product_list:
            arr.append({"product": product, "score": get_product_score(db_object, employee.id, product)})
    else:
        for process in product_list:
            data = (SkillsPR.
                    objects.
                    filter(employee_id=employee.id, process_id=process).
                    values_list("level_id", flat=True))
            arr.append({"process": process, "level": data[0]})
    return arr


def get_product_score(db_object: type[SkillsHW | SkillsSW | SkillsPR], employee_id, product):
    data = (db_object.
            objects.
            filter(employee_id=employee_id, product_id=product).
            values_list("level_id", flat=True))
    score = 0
    for i in data:
        score += level_vals[i]
    return score


def get_object_for_filter(key: str, _id, _filter):
    if key == "hw":
        obj = SkillsHW.objects.filter(employee_id=_id,
                                      product=_filter["product"],
                                      task=_filter["task"]).get()
        return obj
    elif key == "sw":
        obj = SkillsSW.objects.filter(employee_id=_id,
                                      product=_filter["product"],
                                      task=_filter["task"]).get()
        return obj


# Разбить на два?
def get_products_tasks_levels(db_object, employee, product_list, is_long=True):
    """
    Возвращает массив словарей, где 1 словарь - 1 продукт,
    его подкатегории и их уровни, либо же 1 процесс и его уровень

    :param db_object: Объект БД, представляющий таблицу с компетенциями сотрудников по блоку
    :param employee: Объект БД, представляющий работника
    :param product_list: Список продуктов или процессов, для которых нужно собрать информацию
    :param is_long: Ключ, определяющий по какому шаблону будет составлен итоговый массив
    :return: Словари формата [{"product", [("task", "level")...]}, ...] | [{"process", "level"}, ...]
    """
    arr = []
    if is_long:
        for product in product_list:
            data = (db_object.
                    objects.
                    filter(employee_id=employee.id, product_id=product).
                    values_list("task_id", "level_id"))
            tasks = []
            for i in data:
                tasks.append((i[0], i[1]))
            arr.append({"product": product, "tasks": tasks})
    else:
        for process in product_list:
            data = (SkillsPR.
                    objects.
                    filter(employee_id=employee.id, process_id=process).
                    values_list("level_id", flat=True))
            arr.append({"process": process, "level": data[0]})

    return arr
