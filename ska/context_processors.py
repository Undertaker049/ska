from self_assessment.models import Employees
from django.contrib import messages


def user_role(request):

    # Исключение панели суперпользователя из зоны действия контекстного процессора
    if request.path.startswith('/admin'):
        return {}

    if not request.user.is_authenticated:
        return {}

    # Получение объекта сотрудника, связанного с текущим пользователем
    try:
        employee = Employees.objects.get(user=request.user)
        return {'role': employee.role}

    except Employees.DoesNotExist:
        return {}