"""
Django settings for hummus project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ
from django.utils.translation import gettext_lazy as _

# Env basic configuration
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()
DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
DATABASES = {
    'default': env.db(),
}

# Localization and translation
LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fr', _('French')),
]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # extra
    'django_tables2',
    'django_filters',
    'crispy_forms',
    'import_export',
    'microsoft_auth',
    'constance',
    'constance.backends.database',
    # my apps
    'legacy',
    'monitoring',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hummus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # extras
                'microsoft_auth.context_processors.microsoft',
            ],
        },
    },
]

WSGI_APPLICATION = 'hummus.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
 os.path.join(BASE_DIR, "locale"),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

SESSION_COOKIE_DOMAIN = env('SESSION_COOKIE_DOMAIN', default='localhost')

CRISPY_TEMPLATE_PACK = 'bootstrap4'
DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap4.html'

# From https://django-microsoft-auth.readthedocs.io/en/latest/usage.html

AUTHENTICATION_BACKENDS = [
    'microsoft_auth.backends.MicrosoftAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# values you got from step 2 from your Mirosoft app
MICROSOFT_AUTH_CLIENT_ID = env('MICROSOFT_AUTH_CLIENT_ID')
MICROSOFT_AUTH_CLIENT_SECRET = env('MICROSOFT_AUTH_CLIENT_SECRET')

# pick one MICROSOFT_AUTH_LOGIN_TYPE value
# Microsoft authentication
# include Microsoft Accounts, Office 365 Enterpirse and Azure AD accounts
MICROSOFT_AUTH_LOGIN_TYPE = 'ma'

LOGIN_URL = '/admin/login/'

#Jet Menu Settings
JET_SIDE_MENU_ITEMS = [
    {'app_label': 'monitoring', 'items': [
        {'name': 'attendance'},
        {'name': 'contacttype'},
        {'name': 'contact'},
        {'name': 'country'},
        {'name': 'datalist'},
        {'name': 'education'},
        {'name': 'event'},
        {'name': 'filter'},
        {'name': 'organizationtype'},
        {'name': 'organization'},
        {'name': 'product'},
        {'name': 'profile'},
        {'name': 'projectcontact'},
        {'name': 'project'},
        {'name': 'region'},
        {'name': 'structure'},
    ]}
]

#JET dashboard custumization
JET_INDEX_DASHBOARD = 'monitoring.dashboard.CustomIndexDashboard'

# Salesforce settings
SALESFORCE_USERNAME = env('SALESFORCE_USERNAME')
SALESFORCE_PASSWORD = env('SALESFORCE_PASSWORD')
SALESFORCE_TOKEN = env('SALESFORCE_TOKEN')

# Django Constance Dynamic settings
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

try:
    from .constance_settings import *
except ImportError:
    pass
