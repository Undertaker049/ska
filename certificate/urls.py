from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='certificate_main'),
    path('about', views.about, name='certificate_about'),
    path('delete', views.delete_certificate, name='delete_certificate'),
]
