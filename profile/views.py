from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from self_assessment.models import Employees, Department, SkillsHW, SkillsSW, SkillsPR
import http


@login_required
def main(request):

    if request.method == "GET":

        try:
            employee = Employees.objects.get(user=request.user)

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

        except Employees.DoesNotExist:
            messages.error(request, 'Ошибка: профиль сотрудника не найден')
            return redirect('auth:logout')


@login_required
def update(request):

    if request.method != 'POST':
        return HttpResponse(status=http.HTTPStatus.METHOD_NOT_ALLOWED)

    try:
        user = request.user

        if 'username' in request.POST:
            user.username = request.POST.get('username')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()

            try:
                employee = Employees.objects.get(user=user)
                employee.name = f'{user.first_name} {user.last_name}'

                if employee.role != 'admin':
                    department_id = request.POST.get('department')

                    if department_id:
                        employee.department_id = department_id
                employee.save()

            except Employees.DoesNotExist:
                messages.error(request, 'Сотрудник не найден.')
                return redirect('profile:main')

            messages.success(request, 'Профиль успешно обновлен.')

        if 'current_password' in request.POST:
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')

            if not user.check_password(current_password):
                messages.error(request, 'Неверный текущий пароль.')
                return redirect('profile:main')

            user.set_password(new_password)
            user.save()

            messages.success(request, 'Пароль успешно обновлен.')

        return redirect('profile:main')

    except Exception as e:
        messages.error(request, f'Ошибка при обновлении: {str(e)}')
        return redirect('profile:main')