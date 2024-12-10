from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key
from pathlib import Path


class Command(BaseCommand):
    help = 'Generates a new Django secret key and updates .env file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force overwrite existing SECRET_KEY',
        )

    def handle(self, *args, **options):
        env_path = Path('.env')
        new_key = get_random_secret_key()

        if env_path.exists() and not options['force']:

            with open(env_path) as f:

                if 'DJANGO_SECRET_KEY' in f.read():
                    self.stdout.write(
                        self.style.WARNING('SECRET_KEY already exists. Use --force to overwrite')
                    )

                    return

        env_content = []
        if env_path.exists():

            with open(env_path) as f:
                env_content = [
                    line for line in f.readlines()
                    if not line.startswith('DJANGO_SECRET_KEY=')
                ]

                if env_content and not env_content[-1].endswith('\n'):
                    env_content[-1] += '\n'

        env_content.append(f'DJANGO_SECRET_KEY={new_key}\n')

        with open(env_path, 'w') as f:
            f.writelines(env_content)

        self.stdout.write(
            self.style.SUCCESS('Successfully generated new SECRET_KEY')
        )