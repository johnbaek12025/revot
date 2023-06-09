"""
Django settings for barley project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import json

from barley.setting import get_database_info, get_debug_database_info
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
fp = os.path.join(config_dir, 'secret_key')
with open(fp, 'r') as f:
    SECRET_KEY = json.load(f)


# SECURITY WARNING: don't run with debug turned on in production!
fp = os.path.join(config_dir, 'DEBUG')
try:
    with open(fp, 'r') as f:
        DEBUG = json.load(f)
except FileNotFoundError:
    DEBUG = False

fp = os.path.join(config_dir, 'allowed_hosts')
with open(fp, 'r') as f:
    ALLOWED_HOSTS = json.load(f)


fp = os.path.join(config_dir, 'use_server_database')
try:
    with open(fp, 'r') as f:
        USE_SERVER_DATABASE = json.load(f)
except FileNotFoundError:
    print('fp does not exist')
    USE_SERVER_DATABASE = False
_database_config = get_database_info() if USE_SERVER_DATABASE else get_debug_database_info()
DATABASES = _database_config
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'main.apps.MainConfig',
    # 'devoperator.apps.DevoperatorConfig',
    'manager.apps.ManagerConfig',
]

MIDDLEWARE = [    
    'corsheaders.middleware.CorsMiddleware',    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',    
    'django.middleware.common.CommonMiddleware',    
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.filter.CheckAllowedCookie',
]

CORS_ORIGIN_ALLOW_ALL = True
SESSION_COOKIE_SAMESITE = None

ROOT_URLCONF = 'barley.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'barley.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_URL = '/static/'

MEDIAL_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '_media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_ROOT = os.path.join(BASE_DIR, '_staticfilesall')   # cmd: python manage.py collectstatic

LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'log', 'errorLog.log'))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                    'datefmt': "%d/%b/%Y %H:%M:%S"}, 'simple': {'format': '%(levelname)s %(message)s'}, 
                 }, 
    'handlers': {
        'file': {'level': 'DEBUG', 'class': 'logging.handlers.RotatingFileHandler', 'filename': LOG_FILE,
                 'formatter': 'verbose', 'maxBytes': 1024 * 1024 * 10, 'backupCount': 5, }, 
        },
    'loggers': {'django': {'handlers': ['file'], 'propagate': True, 'level': 'ERROR', },
                'django.request': {'handlers': ['file'], 'propagate': False, 'level': 'INFO', },
                'main': {'handlers': ['file'], 'level': 'ERROR', 'propagate': True},
                'devoperator': {'handlers': ['file'], 'level': 'ERROR', 'propagate': True},
                }
}

