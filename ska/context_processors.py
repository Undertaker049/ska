from self_assessment.models import Employees


def user_role(request):
    if not request.user.is_authenticated:
        return {'role': None}

    try:
        return {'role': request.user.employee.role}
    except:
        return {'role': None}