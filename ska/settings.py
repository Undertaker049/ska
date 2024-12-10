"""
Django settings for ska project.
"""

import os
import sys
from pathlib import Path
from django.urls import reverse_lazy
from dotenv import load_dotenv

# Пропуск проверки .env для команд управления окружением
ENVIRONMENT_MANAGEMENT_COMMANDS = ['keygen', 'setenv']
is_env_command = any(cmd in sys.argv for cmd in ENVIRONMENT_MANAGEMENT_COMMANDS)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = BASE_DIR / 'files'

MEDIA_URL = '/files/'

LOGIN_URL = reverse_lazy('auth:login')

LOGIN_REDIRECT_URL = '/'

# Получение SECRET_KEY из переменных окружения
if is_env_command:
    load_dotenv(override=True)
    SECRET_KEY = 'temporary-key-for-env-setup-only'

else:
    if not load_dotenv():
        print("Warning: .env file not found", file=sys.stderr)

    if not os.getenv('DJANGO_SECRET_KEY'):
        raise ValueError(
            "DJANGO_SECRET_KEY must be set in .env file. "
            "Use 'python manage.py setenv' to initialize environment "
            "or 'python manage.py keygen' to generate a new key."
        )
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# Debug mode
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'certificate',
    'employee_evaluation',
    'selection.apps.SelectionConfig',
    'self_assessment',
    'authentication',
    'profile',
    'django_bootstrap5',
    'control.apps.ControlConfig',
    'ska'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'certificate.middleware.CertificateMiddleware',
    'middleware.auth.AuthenticationMiddleware',
    'middleware.background.BackgroundMiddleware',
]

ROOT_URLCONF = 'ska.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ska.context_processors.user_role',
                'ska.context_processors.urls_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'ska.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db' / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (css, JavaScript, Images)
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

if not os.path.exists(STATIC_ROOT):
    os.makedirs(STATIC_ROOT)

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Ensure static files are served in development
if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]
else:
    STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
