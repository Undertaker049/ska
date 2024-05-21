"""
URL configuration for ska project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from certificate import views as certificate_views
from employee_evaluation import views as employee_evaluation_views
from main import views as main_views
from selection import views as selection_views
from self_assessment import views as self_assessment_views
from authentication import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.main),
    path('self-assessment', self_assessment_views.main),
    path('test', self_assessment_views.test),
    path('upload-assessment', self_assessment_views.upload_assessment),
    path('validate-name', self_assessment_views.validate_name),
    path('certificate', certificate_views.main),
    path('employee-evaluation', employee_evaluation_views.main),
    path('selection', selection_views.main),
    path('auth', auth_views.main),
    path('registration', auth_views.registration)
]
