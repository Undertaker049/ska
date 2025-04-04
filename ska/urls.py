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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from certificate import views as certificate_views
from employee_evaluation import views as employee_evaluation_views
from main import views as main_views
from selection import views as selection_views
from self_assessment import views as self_assessment_views
from authentication import views as auth_views
from ska import settings

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', main_views.main),
#     path('self-assessment', self_assessment_views.main),
#     path('self-assessment/upload', self_assessment_views.upload_assessment),
#     path('self-assessment/validate-name', self_assessment_views.validate_name),
#     path('certificate', certificate_views.main),
#     path('certificate/about', certificate_views.about),
#     path('certificate/delete', certificate_views.delete_certificate),
#     path('employee-evaluation', employee_evaluation_views.main),
#     path('employee-evaluation/about', employee_evaluation_views.about),
#     path('employee-evaluation/about-block', employee_evaluation_views.about_block),
#     path('employee-evaluation/reviews', employee_evaluation_views.reviews),
#     path('employee-evaluation/review', employee_evaluation_views.review),
#     path('employee-evaluation/upload-review', employee_evaluation_views.upload_review),
#     path('employee-evaluation/delete-review/<int:review_id>', employee_evaluation_views.delete_review),
#     path('selection', selection_views.main),
#     path('auth', auth_views.main),
#     path('auth/registration', auth_views.registration),
#     path('auth/logout', auth_views.user_logout)
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.main, name='main'),
    path('self-assessment/', include('self_assessment.urls')),
    path('certificate/', include('certificate.urls')),
    path('employee-evaluation/', include('employee_evaluation.urls')),
    path('auth/', include('authentication.urls')),
    path('selection', selection_views.main),
]

# TODO выяснить как работать с файлами в проде
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
