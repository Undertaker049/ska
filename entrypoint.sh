#!/bin/bash

# Убедимся что скрипт завершится при любой ошибке
set -e

# Переходим в директорию приложения
cd /app

# Функция для выполнения Django команд
setup_django() {
    # Собираем статические файлы
    echo 'Collecting static files...'
    python manage.py collectstatic --noinput --clear

    # Применяем миграции
    echo 'Running migrations...'
    python manage.py migrate
}

# Функция запуска сервера
start_server() {
    # Проверяем значение DEBUG в .env
    if grep -q 'DJANGO_DEBUG=True' .env; then
        echo 'Starting development server...'
        python manage.py runserver 0.0.0.0:8000
    else
        echo 'Starting release server...'
        python manage.py runrelease
    fi
}

# Проверяем существование .env файла
if [ ! -f .env ]; then
    echo "Warning: .env file does not exist"
    echo "Please create it using the following commands:"
    echo "1. docker compose exec web python manage.py setenv --debug"
    echo "2. docker compose exec web python manage.py keygen --force"

    # Запускаем мониторинг создания .env файла в фоновом режиме
    (
        # Ждем только создание файла, игнорируем модификации
        inotifywait -e create -q /app |
        while read -r directory events filename; do
            if [ "$filename" = ".env" ]; then
                echo ".env file detected, setting up Django..."
                sleep 1  # Даем время на завершение записи файла
                setup_django
                start_server
                break  # Выходим после первого обнаружения файла
            fi
        done
    ) &
else
    setup_django
    start_server
fi

# Держим контейнер запущенным
exec "$@" 