from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sesac_final',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': 3306
    }
}

# ASGI application
ASGI_APPLICATION = 'config.asgi.local.application'
# WSGI application
WSGI_APPLICATION = 'config.wsgi.local.application'