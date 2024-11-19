from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-password/', views.update_password, name='update_password'),
]