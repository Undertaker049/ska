"""Методы для отображения и работы с данными блока certificate"""
import http
import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from self_assessment.models import Employees
from ska import settings

from .models import Certificate, CertificateCategory, CertificateSubCategory


@login_required
def main(request):
    """
    Выводит список сертификатов пользователя и предоставляет возможность загрузить новый.
    :param request: Объект запроса
    :return: GET - загружает страницу с сертификатами, POST - загружает сертификат на сервер
    """
    employee = Employees.objects.filter(name=f'{request.user.first_name} {request.user.last_name}').get()
    if request.method == 'GET':
        certificates = (Certificate.
                        objects.
                        filter(employee=employee.id).
                        values())
        return render(request, "certificate.html", {"certificates": certificates})

    if request.method == 'POST':
        employee = Employees.objects.filter(name=f'{request.user.first_name} {request.user.last_name}').get()

        data = request.POST
        obj = Certificate(employee=employee.id,
                          training_name=data.get("training_name"),
                          training_type=data.get("training_type"),
                          date=data.get("date"),
                          category=CertificateCategory.objects.get(category=data.get("category")),
                          certificate_file=request.FILES["certificate"])
        if data.get("subcategory", -1) != -1:
            obj.sub_category = CertificateSubCategory.objects.get(subcategory=data.get("subcategory"))

        obj.save()
        # with open("D\\:data", "wb+") as destination:
        #     for chunk in f.chunks():
        #         destination.write(chunk)
        return HttpResponse(status=200, content="Сертификат загружен", content_type="text/*")

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@login_required
def about(request):
    """
    Предоставляет подробную информацию о сертификате и выводит сам сертификат
    :param request: Объект запроса
    :return: GET - страница с сертификатом
    """
    if request.method == 'GET':
        employee = Employees.objects.filter(name=f'{request.user.first_name} {request.user.last_name}').get()
        c = Certificate.objects.filter(employee=employee.id,
                                       id=request.GET.get("id"))
        if c:
            c = c.values()[0]
            data = {"id": c["id"],
                    "name": c["training_name"],
                    "type": c["training_type"],
                    "date": c["date"],
                    "category": c["category_id"],
                    "subcategory": c["sub_category_id"],
                    "file": f"{settings.MEDIA_URL}{c['certificate_file']}",
                    "is_pdf": True if c['certificate_file'].split(".")[1] == "pdf" else False}
            return render(request, 'certificate_about.html', {"certificate": data})
        else:
            return render(request, "certificate_about_not_found.html")

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)


@login_required
def delete_certificate(request):
    """
    Удаляет сертификат, принадлежащий конкретному пользователю
    :param request: Объект запроса
    :return: POST - Удаляет сертификат
    """
    if request.method != "POST":
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    employee = Employees.objects.filter(name=f'{request.user.first_name} {request.user.last_name}').get()
    obj = Certificate.objects.filter(employee=employee.id, id=request.POST["id"]).get()
    if obj.exists():
        path = f"{settings.MEDIA_ROOT}/{obj['certificate_file']}"
        print(path)
        if os.path.isfile(path):
            os.remove(path)
            obj.delete()
            return HttpResponse(status=200, content="Сертификат удален")
        else:
            return HttpResponse(status=http.HTTPStatus.NOT_FOUND, content="Файл сертификата не найден.")
    else:
        return HttpResponse(status=http.HTTPStatus.NOT_FOUND, content="Запись не найдена на сервере.")
