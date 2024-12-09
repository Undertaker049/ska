from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlparse
from django.urls import reverse_lazy


class AuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            public_urls = [
                reverse_lazy('auth:login'),
                reverse_lazy('auth:registration'),
                '/static/',
                '/media/',
                '/admin/',
                '/favicon.ico'
            ]

            current_url = request.path_info

            if (current_url.startswith(str(reverse_lazy('auth:login'))) and
                current_url != str(reverse_lazy('auth:login')) and
                current_url not in [str(reverse_lazy('auth:registration')), str(reverse_lazy('auth:registration'))[:-1]]):
                return redirect('auth:login')

            # Проверка того, является ли текущий URL страницей входа
            if current_url in [str(reverse_lazy('auth:login')), str(reverse_lazy('auth:login'))[:-1]]:
                return self.get_response(request)

            # Проверка остальных публичных URL
            if not any(current_url.startswith(str(url)) for url in public_urls):
                next_url = request.get_full_path()

                # Проверка безопасности next_url
                parsed_next = urlparse(next_url)

                if (not parsed_next.netloc and
                    not parsed_next.scheme and
                    not next_url.startswith(str(reverse_lazy('auth:login'))) and
                    not any(next_url.startswith(str(url)) for url in public_urls)):
                    login_url = f"{settings.LOGIN_URL}?next={next_url}"

                else:
                    login_url = settings.LOGIN_URL

                return redirect(login_url)

        return self.get_response(request)