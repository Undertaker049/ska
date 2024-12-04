from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.main, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.user_logout, name='logout'),
]
