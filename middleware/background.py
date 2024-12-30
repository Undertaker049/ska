"""
Middleware для управления фоновыми изображениями страниц.

Обеспечивает автоматическое наследование фонов дочерними страницами от родительских.
Например, если для '/parent/' установлен фон 'parent_bg.jpg', то все страницы вида
'/parent/child/', '/parent/child/subchild/' и т.д. будут использовать тот же фон,
если для них явно не указан другой.
"""

import os
from django.conf import settings
from django.urls import reverse_lazy


class BackgroundMiddleware:
    """
    Middleware для управления фоновыми изображениями страниц.

    Attributes:
        backgrounds (dict): Словарь соответствия URL-путей и фоновых изображений.
        default_bg (str): Имя файла фонового изображения по умолчанию.
    """

    def __init__(self, get_response):
        """
        Инициализация middleware.

        Args:
            get_response: Следующий обработчик в цепочке middleware.
        """
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

    def get_background_for_path(self, path):
        """
        Определяет фоновое изображение для заданного пути.

        Алгоритм:
        1. Проверяет точное совпадение пути
        2. Если не найдено, ищет ближайший родительский путь
        3. Если ничего не найдено, возвращает фон по умолчанию

        Args:
            path (str): URL-путь, для которого нужно определить фон

        Returns:
            str: Имя файла фонового изображения
        """
        
        # Проверка точного совпадения пути
        if path in self.backgrounds:
            return self.backgrounds[path]

        # Поиск ближайшего родительского пути с фоном
        path_parts = path.rstrip('/').split('/')
        while path_parts:
            parent_path = '/'.join(path_parts) + '/'
            if parent_path in self.backgrounds:
                return self.backgrounds[parent_path]
            path_parts.pop()

        return self.default_bg

    def __call__(self, request):
        """
        Обработка запроса.

        Добавляет к объекту запроса атрибут background_image с путем к фоновому изображению.

        Args:
            request: Объект HTTP-запроса

        Returns:
            HttpResponse: Ответ от следующего обработчика в цепочке middleware
        """
        bg_name = self.get_background_for_path(request.path)
        request.background_image = f'/static/background/images/{bg_name}'
        return self.get_response(request)