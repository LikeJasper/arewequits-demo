# -*- coding: utf-8 -*-
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['likejasper.pythonanywhere.com']

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/LikeJasper/sites/likejasper.pythonanywhere.com/database/db.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}

# Static files

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../../static/'))

# Media

MEDIA_ROOT = os.path.join(BASE_DIR, '../../media/')

# Emails

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'arewequits@gmail.com'
EMAIL_HOST_PASSWORD = get_env_variable('GMAIL_PASSWORD')
EMAIL_PORT = 587
