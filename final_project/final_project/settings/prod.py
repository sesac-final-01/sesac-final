from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sesac_final_db',
        'USER': 'admin',
        'PASSWORD': 'Test1752',
        'HOST': 'final-db-cluster.cluster-ch04q4wsyp2q.ap-northeast-2.rds.amazonaws.com',
        'PORT': 3306,
    }
}

# ASGI application
ASGI_APPLICATION = 'config.asgi.prod.application'
# WSGI application
WSGI_APPLICATION = 'config.wsgi.prod.application'

