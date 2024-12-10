from django.core.management.base import BaseCommand
import os
import shutil
from pathlib import Path


class Command(BaseCommand):
    help = 'Creates .env file from .env.example template'

    def add_arguments(self, parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Set DEBUG=True in created .env file',
        )

    def handle(self, *args, **options):
        example_path = '.env.example'
        env_path = '.env'

        if not os.path.exists(example_path):
            self.stdout.write(self.style.ERROR(f'File {example_path} not found'))
            return

        if os.path.exists(env_path):
            overwrite = input('.env file already exists. Overwrite? (y/n): ')
            if overwrite.lower() != 'y':
                self.stdout.write(self.style.WARNING('Operation cancelled'))
                return

        try:
            # Копирование шаблона
            shutil.copy2(example_path, env_path)

            # Переключение DEBUG, если необходимо
            if options['debug']:
                env_path = Path(env_path)
                content = env_path.read_text()
                content = content.replace('DJANGO_DEBUG=False', 'DJANGO_DEBUG=True')
                env_path.write_text(content)
                debug_status = 'DEBUG=True'

            else:
                debug_status = 'DEBUG=False'

            self.stdout.write(
                self.style.SUCCESS(
                    f'File {env_path} successfully created with {debug_status}. '
                    f'Use python manage.py keygen to generate SECRET_KEY'
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating file: {str(e)}')) 