from self_assessment.models import Employees
from django.contrib import messages
from django.urls import reverse


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


def urls_processor(request):
    """
    Добавляет URLs для использования в JavaScript
    """
    return {
        'urls': {
            'profile_update': reverse('profile:update'),
            'self_assessment_upload': reverse('upload_assessment'),
            'selection_disciplines': reverse('selection_disciplines', args=['0']).replace('0', ''),
            'selection_employees': reverse('selection_employees'),
            'employee_evaluation_subordinates': reverse('employee_evaluation_subordinates'),
            'employee_evaluation_subordinates_filter': reverse('employee_evaluation_subordinates'),
            'employee_evaluation_about': reverse('employee_evaluation_about'),
            'employee_evaluation_about_block': reverse('employee_evaluation_about_block'),
            'certificate_delete': reverse('delete_certificate'),
            'certificate_main': reverse('certificate_main'),
            'auth_login': reverse('auth:login'),
            'auth_registration': reverse('auth:registration'),
        }
    }