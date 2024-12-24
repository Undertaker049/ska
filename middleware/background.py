import os
from django.conf import settings
from django.urls import reverse_lazy


class BackgroundMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.backgrounds = {
            str(reverse_lazy('profile:main')): 'profile_bg.jpg',
            str(reverse_lazy('auth:login')): 'auth_bg.jpg',
            str(reverse_lazy('auth:registration')): 'auth_bg.jpg',
            str(reverse_lazy('self_assessment')): 'self_assessment_bg.jpg',
            str(reverse_lazy('certificate_main')): 'certificate_bg.jpg',
            str(reverse_lazy('employee_evaluation_main')): 'employee_evaluation_bg.jpg',
        }
        self.default_bg = 'main_bg.jpg'

    def __call__(self, request):
        bg_name = self.backgrounds.get(request.path, self.default_bg)
        request.background_image = f'/static/background/images/{bg_name}'
        return self.get_response(request)