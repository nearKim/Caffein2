from django.contrib.messages import constants

DEBUG = True

# Messaging
MESSAGE_LEVEL = constants.DEBUG  # 지금부터 debug 레벨의 messages 를 남길 수 있음.
MESSAGE_TAGS = {constants.ERROR: 'danger'}

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

# EMAIL provider
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'cheshire0814@gmail.com'
# EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = 587
