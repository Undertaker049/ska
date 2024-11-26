from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from self_assessment.models import Employees


def role_required(allowed_roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            employee = Employees.objects.get(
                name=f"{request.user.first_name} {request.user.last_name}"
            )

            if employee.role == 'admin':
                return view_func(request, *args, **kwargs)

            if employee.role not in allowed_roles:
                messages.error(request, 'Ошибка: Недостаточно прав для доступа к функциям администратора')
                return redirect('/')

            if employee.role == 'supervisor':
                dept_id = request.GET.get('department_id')

                if dept_id and int(dept_id) != employee.department_id:
                    return HttpResponseForbidden("Доступ только к своему отделу")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator