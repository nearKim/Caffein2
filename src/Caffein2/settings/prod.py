from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


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

# NaverMap
NAVER_CLIENT_ID = os.environ['NAVER_CLIENT_ID']
NAVER_CLIENT_SECRET = os.environ['NAVER_CLIENT_SECRET']
# Legacy NaverMap support
LEGACY_NAVER_CLIENT_ID = os.environ['LEGACY_NAVER_CLIENT_ID']
LEGACY_NAVER_CLIENT_SECRET = os.environ['LEGACY_NAVER_CLIENT_SECRET']

# AWS
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = 'caffein-prod-assets'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Caffein2/static'),
]
DEFAULT_FILE_STORAGE = 'Caffein2.settings.storage_backend.MediaStorage'

# RDS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'caffein-db.cmuqfrbw8kv7.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
        'NAME': 'caffein',
        'USER': 'caffein_admin',
        'PASSWORD': os.environ['RDS_PASS'],
    }
}

# Unified sentry
sentry_sdk.init(
    dsn="https://10fd27bd517647c69fd07c69793bb653@sentry.io/1306729",
    integrations=[DjangoIntegration()]
)

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

# Prod needs this
ALLOWED_HOSTS = ['*']
