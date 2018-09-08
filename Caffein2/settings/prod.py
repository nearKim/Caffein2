from .base import *
import django_heroku
import dj_database_url
import raven

# RAVEN
RAVEN_CONFIG = {
    'dsn': 'https://539eede31021486b906abc8f34c84956:8969132bf49240beb2992d5dcf41b065@sentry.io/1277131',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': os.environ['SOURCE_VERSION']
}

from raven.contrib.django.raven_compat.models import client

client.captureException()

# Prod needs this
ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

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

# Roots
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = 'snucoffee@gmail.com'
if DEBUG:
    EMAIL_HOST_PASSWORD = get_secret('GMAIL_PASS')
else:
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
