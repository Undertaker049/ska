#!/bin/bash

# Инициализация цветовых констант
YELLOW=$(TERM=xterm-256color tput setaf 3)
RESET=$(TERM=xterm-256color tput sgr0)

cd /app

load_env() {
    if [ -f .env ]; then
        echo "Loading environment variables from .env file..."
        set -a
        source .env
        set +a
    fi
}

setup_django() {
    echo 'Collecting static files...'
    python manage.py collectstatic --noinput --clear

    echo 'Running migrations...'
    python manage.py migrate
}

run_server() {
    if grep -q 'DJANGO_DEBUG=True' .env; then
        echo 'Starting development server...'
        python manage.py runserver 0.0.0.0:8000
    else
        echo 'Starting release server...'
        python manage.py runrelease
    fi
}

start() {
    load_env
    setup_django
    run_server
}

monitor_env() {
    echo "Starting .env file monitoring..."
    (
        while true; do
            if [ ! -f .env ]; then
                echo "Waiting for .env file to be created..."
                inotifywait -e create,moved_to -q /app
                if [ -f .env ]; then
                    echo "${YELLOW}WARNING: .env file was created. Please restart container to apply changes${RESET}"
                fi
            else
                echo "Watching .env file for changes..."
                inotifywait -e modify,delete,move,close_write -q /app/.env
                if [ -f .env ]; then
                    echo "${YELLOW}WARNING: .env file was modified${RESET}"
                    echo "${YELLOW}Please restart container to apply changes${RESET}"
                else
                    echo "${YELLOW}WARNING: .env file was deleted${RESET}"
                fi
            fi
        done
    ) &
}

# Первоначальная настройка и запуск
if [ -f .env ]; then
    start
else
    echo "${YELLOW}WARNING: .env file does not exist${RESET}"
    echo "${YELLOW}Please create it by using the 'python manage.py setenv' command${RESET}"
fi

# Запуск мониторинга в фоне
monitor_env &
exec tail -f /dev/null