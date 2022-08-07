"""
Django settings for hrm project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from decouple import config, Csv
import os
from storages.backends.s3boto3 import S3Boto3Storage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6l6ewf7z^lnxc+3jp8be26ae+3y4y-f=$&lw$*o3*vj#o=buo-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost, 127.0.0.1', cast=Csv())

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_countries',
    'rest_framework',
    'knox',
    "corsheaders",
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = 'hrm.urls'

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

WSGI_APPLICATION = 'hrm.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

POSTGRESQL = config('POSTGRESQL', cast=bool, default=False)

if POSTGRESQL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', cast=str),
            'USER': config('DB_USER', cast=str),
            'PASSWORD': config('DB_PASSWORD', cast=str),
            'HOST': config('DB_HOST', cast=str),
            'PORT': config('DB_PORT', cast=str),
            'TEST': {
                'NAME': config('TEST_DB_NAME', 'kashboitest'),
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = (
    os.path.join(os.path.join(BASE_DIR, 'api'), 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# These are optional -- if they're set as environment variables they won't
# need to be set here as well
# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', None)
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', None)

# Additionally, if you are not using the default AWS region of us-east-1,
# you need to specify a region, like so:
# AWS_SES_REGION_NAME = 'us-west-2'
# AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'
#
# AWS_SES_ACCESS_KEY_ID = config('AWS_SES_ACCESS_KEY_ID', None)
# AWS_SES_SECRET_ACCESS_KEY = config('AWS_SES_SECRET_ACCESS_KEY', None)
# AWS_SES_AUTO_THROTTLE = 1  # safety factor applied to rate limit; default=5
# AWS_SES_CONFIGURATION_SET = 'my-configuration-set-name'


# S3_ENABLED = config('ENABLE_S3', default=True, cast=bool)
#
# if S3_ENABLED:
#     # AWS
#     AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
#     AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
#     AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
#     AWS_DEFAULT_ACL = 'public-read'
#     AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME+'.s3.amazonaws.com'
#     AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
#     AWS_LOCATION = 'static'
#     STATIC_URL = "https://s3.amazonaws.com/%s/static/" % AWS_STORAGE_BUCKET_NAME
#     # STATICFILES_DIRS
#     # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#     AWS_QUERYSTRING_AUTH = False
#     AWS_S3_FILE_OVERWRITE = False
#
#     # # STORAGE
#     # # DEFAULT_FILE_STORAGE=backend.storage.MediaStorage
#     # # STATICFILES_STORAGE =backend.storage.StaticStorage
#     # STATICFILES_LOCATION = config('STATICFILES_LOCATION', default='static')
#     # MEDIAFILES_LOCATION = config('MEDIAFILES_LOCATION', default='media')
#     # DEFAULT_FILE_STORAGE = config(
#     #     'DEFAULT_FILE_STORAGE',
#     #     default='django.core.files.storage.FileSystemStorage'
#     # )
#     # STATICFILES_STORAGE = config(
#     #     'STATICFILES_STORAGE',
#     #     default='django.contrib.staticfiles.storage.staticfiles_storage'
#     # )
#     STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#     DEFAULT_FILE_STORAGE = 'hrm.storage.MediaStorage'


CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = ()
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:9000"
]
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # <-- And here
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],

    # 'PAGE_SIZE': 20,
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'NON_FIELD_ERRORS_KEY': 'errors',

}
REST_KNOX = {'TOKEN_TTL': None}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'emran@mbsoftwarebd.com'
EMAIL_HOST_PASSWORD = 'rayhan08205046'
