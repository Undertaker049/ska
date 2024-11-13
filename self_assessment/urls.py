from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='self_assessment'),
    path('old', views.old, name='self_assessment_old'),
    path('upload', views.upload_assessment, name='upload_assessment'),
    path('validate-name', views.validate_name, name='validate_name')
]
