from .base import *
import facebook

# Facebook
# snucoffee계정
APP_ID = get_secret('FACEBOOK_APP_ID')
APP_SECRET = get_secret('FACEBOOK_APP_SECRET')
# FIXME: 이 그룹은 현재 snucoffee계정이 가입한 django_test 그룹이다.
FACEBOOK_GROUP_ID = '542458402875116'  # django_test
# FIXME: 이 토큰은 2개월후 만료된다.
FACEBOOK_TOKEN = get_secret('FACEBOOK_APP_TOKEN_60')

# AWS
AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'caffein-assets'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

DEFAULT_FILE_STORAGE = 'Caffein2.settings.storage_backend.MediaStorage'

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
