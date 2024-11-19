from django.shortcuts import redirect
from django.conf import settings


class AuthenticationMiddleware:


    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):

        if not request.user.is_authenticated:
            public_urls = [
                '/auth/registration',
                '/static/',
                '/media/',
                '/favicon.ico'
            ]

            current_url = request.path_info

            if not any(current_url.startswith(url) for url in public_urls) and current_url != settings.LOGIN_URL:
                next_url = request.get_full_path()
                login_url = f"{settings.LOGIN_URL}?next={next_url}"
                return redirect(login_url)

        response = self.get_response(request)
        return response