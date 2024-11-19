from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='auth_main'),
    path('registration', views.registration, name='registration'),
    path('logout', views.user_logout, name='logout'),
]
