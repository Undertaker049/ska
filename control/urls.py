from django.urls import path
from . import views

app_name = 'control'

urlpatterns = [
    path('', views.admin_index, name='index'),
    path('statistics/', views.statistics, name='statistics')
]