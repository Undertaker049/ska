from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from ska.decorators import role_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from self_assessment.models import Department, Employees
from certificate.models import Certificate


@login_required
@role_required(['admin'])
def admin_index(request):
    return redirect('admin:statistics')


@login_required
@role_required(['admin'])
def statistics(request):
    try:
        # Базовая статистика
        context = {
            'total_users': User.objects.count(),
            'total_departments': Department.objects.count(),
            'total_certificates': Certificate.objects.count(),

            # Данные для графика отделов
            'departments_data': {
                'labels': list(Department.objects.values_list('name', flat=True)),
                'data': list(Department.objects.annotate(
                    count=Count('employees')).values_list('count', flat=True))
            }
        }

        return render(request, 'statistics.html', context)

    except Exception as e:
        print(f"Error in statistics view: {str(e)}")
        import traceback
        traceback.print_exc()
        return HttpResponseForbidden("Произошла ошибка при загрузке статистики")