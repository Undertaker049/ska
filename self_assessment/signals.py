from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import connection
import os
from termcolor import colored
import sys


@receiver(post_migrate)
def initialize_database(sender, **kwargs):
    """
    Сигнал для автоматической инициализации базы данных после выполнения миграций
    """

    if sender.name != 'self_assessment':
        return

    try:
        sql_file_path = os.path.join('db', 'ska-init.sql')

        if not os.path.exists(sql_file_path):
            print(colored(f'Error: SQL file not found at {sql_file_path}', 'red', attrs=['bold']), file=sys.stderr)
            return

        # Чтение БД
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Выполнение SQL скрипта
        with connection.cursor() as cursor:
            cursor.executescript(sql_content)

        print(colored('Database initialized successfully from ska-init.sql', 'green', attrs=['bold']))

    except Exception as e:
        print(colored(f'Error initializing database: {str(e)}', 'red', attrs=['bold']), file=sys.stderr)