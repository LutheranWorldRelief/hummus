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
from django.utils.log import DEFAULT_LOGGING

# Env basic configuration
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()
DEBUG = env('DEBUG')
ADMINS = [x.split(':') for x in env.list('DJANGO_ADMINS', default=())]
DEFAULT_LOGGING['handlers']['console']['filters'] = []
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
    'django.contrib.gis',
    # extra
    'leaflet',
    'django_tables2',
    'django_filters',
    'crispy_forms',
    'import_export',
    'microsoft_auth',
    'constance',
    'constance.backends.database',
    'rest_framework',
    'django_select2',
    # my apps
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
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hummus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # extras
                'microsoft_auth.context_processors.microsoft',
                'constance.context_processors.config',
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
FORMAT_MODULE_PATH = [ 'formats' ]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, '../static/')
MEDIA_ROOT = os.path.join(BASE_DIR, '../media/')

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
MICROSOFT_DOMAIN = env('MICROSOFT_DOMAIN')

# pick one MICROSOFT_AUTH_LOGIN_TYPE value
# Microsoft authentication
# include Microsoft Accounts, Office 365 Enterpirse and Azure AD accounts
MICROSOFT_AUTH_LOGIN_TYPE = 'ma'

# Jet Menu Settings
JET_SIDE_MENU_ITEMS = [
    {'label': _('Import Beneficiaries'), 'permissions': ['monitoring.add_projectcontact',
                                                         'monitoring.change_projectcontact',
                                                         'monitoring.add_contact',
                                                         'monitoring.change_contact'], 'items': [
        {'name': '', 'url': '/import/participants/step1  ',
         'label': _('Import Beneficiaries')},
    ]},
    {'label': _('Participants'), 'permissions': ['monitoring.view_contact'], 'items': [
        {'name': 'monitoring.contact', 'label': _('Participants'),
         'permissions': ['monitoring.view_contact']},
        {'name': '', 'url': '/validate/dupes-name', 'label': _('Duplicates by Name'),
         'permissions': ['monitoring.change_contact', 'monitoring.change_projectcontact']},
        {'name': '', 'url': '/validate/dupes-doc', 'label': _('Duplicates per document'),
         'permissions': ['monitoring.change_contact', 'monitoring.change_projectcontact']},
    ]},
    {'label': _('Reports'), 'permissions': ['monitoring.view_projectcontact',
                                            'monitoring.view_country',
                                            'monitoring.view_contact',
                                            'monitoring.view_organization'], 'items': [
        {'name': '', 'url': '/export/participants', 'label': _('Project Participants')},
        {'name': '', 'url': '/export/template-clean/', 'label': _('Clean Template'),
         'permissions': ['monitoring.add_projectcontact',
                         'monitoring.change_projectcontact',
                         'monitoring.add_contact',
                         'monitoring.change_contact']},
    ]},
    {'label': _('Dashboard'), 'items': [
        {'name': '', 'url': '/dashboard/', 'label': _('Dashboard')},
    ]},
    {'label': _('Configurations'), 'items': [
        {'name': 'monitoring.project', 'label': _('Projects'), 'permissions': [
            'monitoring.view_project']},
        {'name': 'monitoring.organization', 'label': _('Organizations'),
         'permissions': ['monitoring.view_organization']},
        {'name': 'monitoring.organizationtype', 'label': _('Types'),
         'permissions': ['monitoring.view_organizationtype']},
        {'name': 'monitoring.country', 'label': _('Countries'), 'permissions': [
            'monitoring.view_country']},
        {'name': 'monitoring.contacttype', 'label': _('Contact Types'), 'permissions': [
            'monitoring.view_contacttype']},
        {'name': 'monitoring.education', 'label': _('Educations'), 'permissions': [
            'monitoring.view_education']},
        {'name': 'monitoring.sex', 'label': _('Sex'), 'permissions': ['monitoring.view_sex']},
        {'name': 'monitoring.lwrregion', 'label': _('Regions'), 'permissions': [
            'monitoring.view_lwrregion']},
        {'name': 'monitoring.filter', 'label': _('Segmentation'), 'permissions': [
            'monitoring.view_filter']},
    ]},
    {'label': _('Security'), 'permissions': ['request.user.is_superuser'], 'items': [
        {'name': 'auth.user', 'label': _('Users')},
        {'name': 'auth.group', 'label': _('Roles')},
        {'name': 'monitoring.profile', 'label': _('Profiles')},
    ]}
]

# JET dashboard custumization
JET_INDEX_DASHBOARD = 'monitoring.admin_dashboard.CustomIndexDashboard'
# Salesforce settings
SALESFORCE_USERNAME = env('SALESFORCE_USERNAME')
SALESFORCE_PASSWORD = env('SALESFORCE_PASSWORD')
SALESFORCE_TOKEN = env('SALESFORCE_TOKEN')
SALESFORCE_URL = env('SALESFORCE_URL', default='https://example.my.salesforce.com')

# Django Constance Dynamic settings
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

LOGIN_REDIRECT_URL = '/dashboard'

# optional constance settings
try:
    from .constance_settings import *
except ImportError:
    pass

# optional sentry init
try:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[DjangoIntegration()]
    )
except ImportError:
    pass
