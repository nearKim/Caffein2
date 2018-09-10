from .base import *
import facebook

# Facebook
# snucoffee계정
APP_ID = 1960145344283234
APP_SECRET = '377f41d4e8a22eab6d874a1a4ddcc32e'
# FIXME: 이 그룹은 현재 snucoffee계정이 가입한 django_test 그룹이다.
FACEBOOK_GROUP_ID = '542458402875116'  # django_test
# FIXME: 이 토큰은 2개월후 만료된다.
FACEBOOK_TOKEN = 'EAAb2veb0QmIBALZBusSFIlhPBSnDIPWVDLrzciiIIntKEsZCHSZAWNMZAUAeHtZCatzl1FUDhmPupSSZBMF4pNWUnFH5TE98EPGhX9qoUAUV3wGLNkpvZC4WIlI0fieVRWYEaZA1eYLy97qytfqnCZCJt1SDqdZCsfYZB4ZD'

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
