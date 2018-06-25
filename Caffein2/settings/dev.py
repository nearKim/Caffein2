from .base import *
from django.contrib.messages import constants

DEBUG = True

# Messaging
MESSAGE_LEVEL = constants.DEBUG  # 지금부터 debug 레벨의 messages 를 남길 수 있음.
MESSAGE_TAGS = {constants.ERROR: 'danger'}

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}