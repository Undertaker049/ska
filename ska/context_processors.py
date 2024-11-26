from self_assessment.models import Employees


def user_role(request):
    if not request.user.is_authenticated:
        return {'role': None}

    try:
        employee = Employees.objects.get(
            name=f"{request.user.first_name} {request.user.last_name}"
        )
        return {'role': employee.role}
    except Employees.DoesNotExist:
        return {'role': None}