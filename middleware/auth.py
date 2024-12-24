from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlparse
from django.urls import reverse_lazy


class AuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.user.is_authenticated:

            # Получение URL из settings.py с удалением начального слеша
            static_url = settings.STATIC_URL.lstrip('/')
            media_url = settings.MEDIA_URL.lstrip('/')
            admin_url = getattr(settings, 'ADMIN_URL', 'admin/').lstrip('/')

            public_urls = [
                str(reverse_lazy('auth:login')).lstrip('/'),
                str(reverse_lazy('auth:registration')).lstrip('/'),
                static_url,
                media_url,
                admin_url,
            ]

            current_url = request.path_info.lstrip('/')

            # Нормализация URL путем добавления слеша для директорий
            if current_url and not current_url.endswith('/'):
                url_slash = current_url + '/'

            else:
                url_slash = current_url

            # Проверка прямого совпадения с публичными URL
            if any(url in (current_url, url_slash) for url in public_urls):
                return self.get_response(request)

            # Проверка префиксов для статических, медиа и админ URL
            if any(current_url.startswith(url) for url in [static_url, media_url, admin_url]):
                return self.get_response(request)

            next_url = request.get_full_path()
            parsed_next = urlparse(next_url)

            if (not parsed_next.netloc and
                not parsed_next.scheme and
                not next_url.startswith(str(reverse_lazy('auth:login'))) and
                not any(next_url.startswith('/' + url) for url in public_urls)):
                login_url = f"{settings.LOGIN_URL}?next={next_url}"

            else:
                login_url = settings.LOGIN_URL

            return redirect(login_url)

        return self.get_response(request)