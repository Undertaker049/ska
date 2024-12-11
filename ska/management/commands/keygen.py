from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key
from django.conf import settings
import os
import re


class Command(BaseCommand):
    help = 'Generate new SECRET_KEY and update .env file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regenerate SECRET_KEY even if it exists',
        )

    def handle(self, *args, **options):
        if not os.path.exists('.env'):
            self.stderr.write(self.style.ERROR('.env file not found'))
            return

        # Чтение текущего .env файл
        with open('.env', 'r') as f:
            lines = f.readlines()

        # Генерация нового ключа
        secret_key = f'"{get_random_secret_key()}"'

        # Поиск и замена строки с SECRET_KEY в .env
        secret_key_pattern = re.compile(r'^DJANGO_SECRET_KEY=.*$')
        key_found = False

        for i, line in enumerate(lines):

            if secret_key_pattern.match(line):
                current_key = line.split('=')[1].strip().strip('"\'')

                if current_key and not current_key.isspace() and not options['force']:
                    self.stdout.write(self.style.WARNING('SECRET_KEY already exists. Use --force to regenerate.'))
                    return

                lines[i] = f'DJANGO_SECRET_KEY={secret_key}\n'
                key_found = True
                break

        if not key_found:
            lines.append(f'DJANGO_SECRET_KEY={secret_key}\n')

        # Запись обновленного файла
        with open('.env', 'w') as f:
            f.writelines(lines)

        self.stdout.write(self.style.SUCCESS('SECRET_KEY generated'))