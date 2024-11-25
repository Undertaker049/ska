from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from ska.decorators import role_required
from self_assessment.models import Employees, Department
from .forms import EmployeeForm, DepartmentForm
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from .models import UserActivity
from certificate.models import Certificate


@login_required
@role_required(['admin'])
def admin_index(request):
    return redirect('admin:statistics')


@login_required
def statistics(request):

    try:
        if not hasattr(request.user, 'employee') or request.user.employee.role != 'admin':
            return redirect('/')

    except Exception:
        return redirect('/')

    try:
        total_users = User.objects.count()
        total_departments = Department.objects.count()
        total_certificates = Certificate.objects.count()

        departments_data = Department.objects.annotate(
            user_count=Count('employees')
        ).values('name', 'user_count')

        now = timezone.now()
        last_week = now - timedelta(days=7)
        activity_data = UserActivity.objects.filter(
            created_at__gte=last_week
        ).values('created_at').annotate(
            count=Count('id')
        ).order_by('created_at')

        recent_actions = UserActivity.objects.select_related('user').order_by('-created_at')[:10]

        departments_chart_data = {
            'labels': [dept['name'] for dept in departments_data],
            'data': [dept['user_count'] for dept in departments_data]
        }

        activity_chart_data = {
            'labels': [entry['created_at'].strftime('%d.%m') for entry in activity_data],
            'data': [entry['count'] for entry in activity_data]
        }

        context = {
            'total_users': total_users,
            'total_departments': total_departments,
            'total_certificates': total_certificates,
            'recent_actions': recent_actions,
            'departments_data': departments_chart_data,
            'activity_data': activity_chart_data
        }

        return render(request, 'statistics.html', context)

    except Exception as e:
        # В продакшене лучше использовать логгер для записи ошибок
        print(f"Error in statistics view: {str(e)}")
        return redirect('/')