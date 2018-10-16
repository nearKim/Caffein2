from .base import *
import django_heroku
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

# Facebook
# snucoffee계정
APP_ID = os.environ['FACEBOOK_APP_ID']
APP_SECRET = os.environ['FACEBOOK_APP_SECRET']
# FIXME: 이 그룹은 현재 snucoffee계정이 가입한 django_test 그룹이다.
FACEBOOK_GROUP_ID = '542458402875116'  # django_test
# FIXME: 이 토큰은 2개월후 만료된다.
FACEBOOK_TOKEN = os.environ['FACEBOOK_APP_TOKEN_60']

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Caffein2', 'static'),
]

STATIC_ROOT = 'staticfiles'
MEDIA_ROOT = 'mediafiles'
# Media files

MEDIA_URL = '/media/'
MEDIAFILES_DIRS = [
    os.path.join(BASE_DIR, 'Caffein2', 'media'),
]

# NaverMap
NAVER_CLIENT_ID = os.environ['NAVER_CLIENT_ID']
NAVER_CLIENT_SECRET = os.environ['NAVER_CLIENT_SECRET']

# AWS
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = 'caffein-alpha-assets'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

DEFAULT_FILE_STORAGE = 'Caffein2.settings.storage_backend.MediaStorage'

# Raven
RAVEN_CONFIG = {
    'dsn': 'https://539eede31021486b906abc8f34c84956:8969132bf49240beb2992d5dcf41b065@sentry.io/1277131',
}
# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['sentry'],
            'level': 'WARNING',
            'propagate': True,
        },
        'raven': {
            'level': 'WARNING',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'WARNING',
            'handlers': ['sentry'],
            'propagate': False,
        },
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = 'snucoffee@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Database for Heroku
db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES = {
    'default': db_from_env
}

# DO HEROKU WORK
django_heroku.settings(locals())

# Prod needs this
ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']
