from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.main, name='main'),
    path('update/', views.update, name='update')
]