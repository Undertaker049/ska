from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import connection
import os


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
            print(f'Error: SQL file not found at {sql_file_path}')
            return

        # Чтение БД
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Выполнение SQL скрипта
        with connection.cursor() as cursor:
            cursor.executescript(sql_content)

        print('Database initialized successfully from ska-init.sql')

    except Exception as e:
        print(f'Error initializing database: {str(e)}')