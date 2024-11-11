"""Методы для отображения и работы с данными блока employee evaluation"""
import http
import json
import operator
from array import array

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from certificate.models import Certificate, CertificateCategory, CertificateSubCategory
from self_assessment.models import (Employees, Hardware, Software, Processes, TaskHW, SkillsHW,
                                    TaskSW, SkillsSW, SkillsPR, Levels)
from .models import Reviews

HW_MAX_SCORE = 48
SW_MAX_SCORE = 20

def get_levels_values():
    """Получает словарь уровней и их весов"""
    levels_val = {}
    for o in Levels.objects.values():
        levels_val[o["level"]] = o["weight"]
    return levels_val

def get_products_data():
    """Получает данные о продуктах, задачах и процессах"""
    return {
        'hw_products': Hardware.objects.values_list('product', flat=True),
        'hw_tasks': TaskHW.objects.values_list('task', flat=True),
        'sw_products': Software.objects.values_list('product', flat=True),
        'sw_tasks': TaskSW.objects.values_list('task', flat=True),
        'processes': Processes.objects.values_list('process', flat=True)
    }

def get_certificate_data():
    """Получает данные о категориях сертификатов"""
    return {
        'categories': CertificateCategory.objects.values_list('category', flat=True),
        'subcategories': list(CertificateSubCategory.objects.values_list('subcategory', 'subcategory_of'))
    }


@login_required
def main(request):
    """
    Выводит список сотрудников в виде таблицы, если пользователь - руководитель -
     дополнительно подгружает данные для интерфейса фильтрации подчиненных
    """
    if request.method == "GET":
        employee = Employees.objects.get(name=f"{request.user.first_name} {request.user.last_name}")
        data = {"employees": Employees.objects.values(),
                "is_supervisor": employee.is_supervisor}

        if employee.is_supervisor:
            products_data = get_products_data()
            cert_data = get_certificate_data()
            levels = get_levels_values()

            data.update({
                "hw": products_data['hw_products'],
                "hw_tasks": products_data['hw_tasks'],
                "sw": products_data['sw_products'],
                "sw_tasks": products_data['sw_tasks'],
                "processes": products_data['processes'],
                "certificate_category": cert_data['categories'],
                "certificate_subcategory": cert_data['subcategories'],
                "hw_max": HW_MAX_SCORE,
                "sw_max": SW_MAX_SCORE,
                "levels": levels.keys()
            })

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
    """
    Предоставляет ревью с указанным id
    :param request: Объект запроса
    :return: Текст ревью
    """
    if request.method == "GET":
        return JsonResponse({"data": Reviews.objects.filter(id=request.GET["id"]).values().first()["message"]})
    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@login_required
def delete_review(request, review_id):
    """
    Удаляет выбранное ревью
    :param request: Объект запроса
    :param review_id: id ревью
    :return: Код 200 если удаление прошло успешно
    """
    if request.method != "DELETE":
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    obj = Reviews.objects.get(id=review_id)
    employee_id = Employees.objects.get(name=f"{request.user.first_name} {request.user.last_name}").id
    if obj.reviewer_id == employee_id:
        obj.delete()
        return HttpResponse(status=http.HTTPStatus.OK)

    return HttpResponse(status=http.HTTPStatus.FORBIDDEN, content="Нельзя удалить чужое ревью!")


@login_required
def upload_review(request):
    """
    Загружает ревью
    :param request: Объект запроса
    :return: Код 200 если загрузка успешна
    """
    if request.method != "POST":
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

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

    obj.save()
    return HttpResponse(status=200)


@login_required
def get_subordinates(request):
    """
    Предоставляет список id сотрудников, являющихся подчиненными отправившего запрос
    :param request: Объект запроса
    :return: Список id подчиненных
    """
    employee = Employees.objects.get(name=f"{request.user.first_name} {request.user.last_name}")
    return JsonResponse(
        {"data": list(Employees.objects.filter(subordinate_of=employee.id).values_list('id', flat=True))})


@login_required
def subordinates_apply_filters(request):
    """
    Фильтрует подчиненных по запрошенным фильтрам
    :param request: Объект запроса
    :return: Список подчиненных прошедших фильтры или id фильтра, после которого фильтровать больше некого
    """
    if request.method != "POST":
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    data = json.loads(request.POST.get("data"))
    filters = data["filters"]
    subordinates = list(Employees.objects.filter(id__in=data["subordinates"]).values())
    sub_to_remove = []
    data_for_table = {key: [] for key in data["subordinates"]}
    levels_val = get_levels_values()

    for _id in filters:
        _filter = filters[_id]
        if _filter["block"] in ["hw", "sw"]:
            if _filter["task"] != "Total":
                for index, subordinate in enumerate(subordinates):
                    try:
                        model = SkillsHW if _filter["block"] == "hw" else SkillsSW
                        obj = model.objects.get(
                            employee_id=subordinate["id"],
                            product=_filter["product"],
                            task=_filter["task"]
                        )

                        if compare_to_filter(
                            _filter["sign"],
                            levels_val[obj.level_id],
                            levels_val[_filter["value"]]
                        ):
                            data_for_table[subordinate["id"]].append(obj.level_id)
                            continue

                    except model.DoesNotExist:
                        pass

                    sub_to_remove.append(index)

            elif _filter["task"] == "Total":
                for index, subordinate in enumerate(subordinates):
                    model = SkillsHW if _filter["block"] == "hw" else SkillsSW
                    score = get_product_score(model, subordinate["id"], _filter["product"])

                    if compare_to_filter(_filter["sign"], score, int(_filter["value"])):
                        data_for_table[subordinate["id"]].append(score)
                        continue
                    sub_to_remove.append(index)

        elif _filter["block"] == "pr":
            for index, subordinate in enumerate(subordinates):
                try:
                    obj = SkillsPR.objects.get(
                        process=_filter["process"],
                        employee_id=subordinate["id"]
                    )
                    if compare_to_filter(
                        _filter["sign"],
                        levels_val[obj.level_id],
                        levels_val[_filter["value"]]
                    ):
                        data_for_table[subordinate["id"]].append(obj.level_id)
                        continue

                except SkillsPR.DoesNotExist:
                    pass

                sub_to_remove.append(index)

        elif _filter["block"] == "cr":
            certificates = Certificate.objects.filter(category=_filter["category"])
            if _filter["subcategory"] != "any":
                certificates = certificates.filter(sub_category=_filter["subcategory"])

            for index, subordinate in enumerate(subordinates):
                if certificates.filter(employee_id=subordinate["id"]).exists():
                    subcategory = certificates.filter(employee_id=subordinate["id"]).first().sub_category
                    data_for_table[subordinate["id"]].append(str(subcategory) if subcategory else "N/A")
                    continue

                sub_to_remove.append(index)

        if sub_to_remove:
            subordinates = [subordinates[i] for i, _ in enumerate(subordinates) if i not in sub_to_remove]
            sub_to_remove.clear()

        if not subordinates:
            return HttpResponse(status=http.HTTPStatus.NOT_FOUND, content=_id)

    return JsonResponse(
        status=http.HTTPStatus.OK,
        data={
            "employees_id": [subordinate["id"] for subordinate in subordinates],
            "data_for_table": data_for_table
        }
    )

# Вынести все вспомогательные функции в отдельный файл
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


def get_products_scores(db_object: type[SkillsHW | SkillsSW | SkillsPR], employee: Employees,
                        product_list: array, is_long=True):
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
    """
    Считает суммарное значение, представляющее общие знания о дисциплине
    """
    data = (db_object.
            objects.
            filter(employee_id=employee_id, product_id=product).
            values_list("level_id", flat=True))
    levels_val = get_levels_values()
    score = 0
    for i in data:
        score += levels_val[i]
    return score

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


def compare_to_filter(sign: str, val1: int, val2: int) -> bool:
    """
    Сравнивает значения по нужному знаку.
    :param sign: Знак
    :param val1: Число 1
    :param val2: Число 2
    :return: True - знак корректен. False - знак некорректен
    """
    operators = {
        '<': operator.lt,
        '>': operator.gt,
        '=': operator.eq,
    }
    return operators.get(sign)(val1, val2)
