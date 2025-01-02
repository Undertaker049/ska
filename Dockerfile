# Использование официальный образа Python 3.12 slim для минимального размера
FROM python:3.12-slim

# Установка системных зависимостей и настройка Apache
# - gcc: для компиляции Python-пакетов
# - inotify-tools: для мониторинга изменений файлов
# - curl: для загрузки внешних ресурсов
# - dos2unix: для нормализации конфигурационных файлов
# - apache2 и apache2-utils: веб-сервер и утилиты
# - libxml2-dev: для работы с XML
RUN apt-get update \
    && apt-get install -y \
        gcc \
        inotify-tools \
        curl \
        dos2unix \
        apache2 \
        apache2-utils \
        libxml2-dev \

    # Включение необходимых модулей Apache
    && a2enmod proxy \
    && a2enmod proxy_http \
    && a2enmod proxy_balancer \
    && a2enmod lbmethod_byrequests \
    && a2enmod headers \
    && a2enmod expires \
    && a2enmod alias \
    && a2enmod mime \

    # Очистка кэша apt для уменьшения размера образа
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \

    # Фиксация версий curl и dos2unix
    && apt-mark hold curl dos2unix \

    # Создание и настройка директорий для логов Apache
    && mkdir -p /var/log/apache2 \
    && mkdir -p /var/run/apache2 \
    && chown -R www-data:www-data /var/log/apache2 \
    && chown -R www-data:www-data /var/run/apache2

# Установка рабочей директории
WORKDIR /app

# Создание необходимых директорий и настройка прав доступа
# - /app/db: для SQLite базы данных
# - /app/files: для медиа-файлов
# - /app/static/vendor: для внешних библиотек
RUN mkdir -p /app/db /app/files /app/static/vendor \
    && chmod -R 755 /app/static \
    && chown -R www-data:www-data /app/static

# Копирование файлов проекта
COPY . .

# Нормализация конфигурационных файлов (конвертация CRLF в LF)
RUN dos2unix .vendors .requirements || true

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r .requirements

# Создание и настройка директории для статических файлов
# Права 755 позволяют Apache читать и выполнять, но не изменять файлы
RUN mkdir -p /app/staticfiles \
    && chown -R www-data:www-data /app/staticfiles \
    && chmod -R 755 /app/staticfiles

# Открытие портов:
# - 80: для Apache (обработка статических файлов и проксирование)
EXPOSE 80

# Запуск оболочки по умолчанию (фактический запуск серверов происходит через entrypoint.sh)
CMD ["sh"]