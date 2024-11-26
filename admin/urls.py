from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    path('statistics/', views.statistics, name='statistics'),
]