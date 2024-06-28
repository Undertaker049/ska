"""Методы для отображения и работы с данными блока certificate"""
import http
import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from ska import settings

from .models import Certificate, CertificateCategory, CertificateSubCategory


@login_required
def main(request):
    """
    Выводит список сертификатов пользователя и предоставляет возможность загрузить новый.
    :param request: Объект запроса
    :return: GET - загружает страницу с сертификатами, POST - загружает сертификат на сервер
    """
    if request.method == 'GET':
        certificates = (Certificate.
                        objects.
                        filter(employee_name=f'{request.user.first_name} {request.user.last_name}').
                        values())
        return render(request, "certificate.html", {"certificates": certificates})
    if request.method == 'POST':
        data = request.POST
        print(data)
        obj = Certificate(employee_name=f'{request.user.first_name} {request.user.last_name}',
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
        c = Certificate.objects.filter(employee_name=f"{request.user.first_name} {request.user.last_name}",
                                       id=request.GET.get("id"))
        if c:
            c = c.values()[0]
            # sl = CertificateSubCategory.objects.values()
            # selections = {}
            #
            # for elem in sl:
            #     arr = []
            #     for e in sl.filter(subcategory_of_id=elem["subcategory_of_id"]).values():
            #         arr.append(e["subcategory"])
            #     arr.append("(Empty)")
            #     selections[elem["subcategory_of_id"]] = arr

            data = {"id": c["id"],
                    "name": c["training_name"],
                    "type": c["training_type"],
                    # "date": c["date"].strftime('%Y-%m-%d'),
                    "date": c["date"],
                    "category": c["category_id"],
                    "subcategory": c["sub_category_id"],
                    "file": f"{settings.MEDIA_URL}{c['certificate_file']}",
                    "is_pdf": True if c['certificate_file'].split(".")[1] == "pdf" else False}
            # "selections": selections}
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
    if request.method == "POST":
        obj = Certificate.objects.filter(employee_name=f"{request.user.first_name} {request.user.last_name}",
                                         id=request.POST["id"])
        if obj.exists():
            path = f"{settings.MEDIA_ROOT}/{obj.values()[0]['certificate_file']}"
            print(path)
            if os.path.isfile(path):
                os.remove(path)
                obj.delete()
                return HttpResponse(status=200, content="Сертификат удален")
            else:
                return HttpResponse(status=http.HTTPStatus.NOT_FOUND, content="Файл сертификата не найден.")
        else:
            return HttpResponse(status=http.HTTPStatus.NOT_FOUND, content="Запись не найдена на сервере.")

    return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)
