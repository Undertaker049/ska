# Без этого хэдера браузер запрещает отображение файлов,
# по идее нужно только для локального запуска, т.е. для разработки
class CertificateMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Frame-Options"] = "SAMEORIGIN"
        return response
