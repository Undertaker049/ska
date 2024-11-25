from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
import http

from self_assessment.models import Employees, Department
from self_assessment.models import SkillsHW, SkillsSW, SkillsPR


@login_required
def main(request):
    if request.method == "GET":
        employee = Employees.objects.filter(
            name=f'{request.user.first_name} {request.user.last_name}'
        ).get()

        context = {
            'user': request.user,
            'department': employee.department,
            'departments': Department.objects.all(),
            'has_assessments': False,
            'role': employee.role
        }

        hw_results = SkillsHW.objects.filter(employee_id=employee.id)
        sw_results = SkillsSW.objects.filter(employee_id=employee.id)
        pr_results = SkillsPR.objects.filter(employee_id=employee.id)

        if hw_results.exists() or sw_results.exists() or pr_results.exists():
            context.update({
                'has_assessments': True,
                'hw_results': hw_results,
                'sw_results': sw_results,
                'pr_results': pr_results
            })

        return render(request, "profile.html", context)


@login_required
def update_profile(request):
    if request.method != 'POST':
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    try:
        user = request.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        employee = user.employee

        if employee.role != 'admin':
            department_id = request.POST.get('department')
            if department_id:
                employee.department_id = department_id
                employee.save()

        return HttpResponse(status=http.HTTPStatus.OK)

    except Exception as e:
        return HttpResponse(
            status=http.HTTPStatus.BAD_REQUEST,
            content=str(e)
        )


@login_required
def update_password(request):
    if request.method != 'POST':
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    try:
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        if not user.check_password(current_password):
            return HttpResponse(
                status=http.HTTPStatus.BAD_REQUEST,
                content='Неверный текущий пароль'
            )

        user.set_password(new_password)
        user.save()

        return HttpResponse(status=http.HTTPStatus.OK)

    except Exception as e:
        return HttpResponse(
            status=http.HTTPStatus.BAD_REQUEST,
            content=str(e)
        )