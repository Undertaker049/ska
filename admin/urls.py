from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    path('', views.admin_index, name='index'),
    path('statistics/', views.statistics, name='statistics')
]