# -*- coding: utf-8 -*-
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

WSGI_APPLICATION = 'arewequits.wsgi.application'

TEST_RUNNER = 'green.djangorunner.DjangoRunner'
INSTALLED_APPS += (
        'django_behave',
        'behavioral_tests',
    )

# Media

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Emails

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
