from .base import *


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'caffein',
        'USER': 'postgres',
        'PASSWORD': '0814',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# DEBUG toolbar
INTERNAL_IPS = ('127.0.0.1',)

# EMAIL provider
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
