import os
from django.conf import settings


class BackgroundMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.backgrounds_path = os.path.join(settings.STATIC_ROOT, 'background', 'images')
        self.default_bg = '/static/background/images/main_bg.jpg'

        self.page_backgrounds = {
            '/': 'main_bg.jpg',
            '/profile/': 'profile_bg.jpg',
            '/auth/': 'auth_bg.jpg',
            '/auth/registration/': 'auth_bg.jpg',
            '/self-assessment/': 'self_assessment_bg.jpg',
            '/certificate/': 'certificate_bg.jpg',
            '/employee-evaluation/': 'employee_evaluation_bg.jpg',
            '/selection': 'selection_bg.jpg'
        }

    def __call__(self, request):
        background = self.get_background(request.path)
        request.background_image = background
        response = self.get_response(request)
        return response

    def get_background(self, path):

        if path in self.page_backgrounds:
            bg_path = f'/static/background/images/{self.page_backgrounds[path]}'
            physical_path = os.path.join(settings.STATIC_ROOT, 'background', 'images', self.page_backgrounds[path])

            if os.path.exists(physical_path):
                return bg_path

        return self.default_bg