from .base import *

DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/
def get_secret(setting):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        secret_file = os.path.join(BASE_DIR, 'Caffein2', 'secrets.json')
        with open(secret_file) as f:
            secrets = json.loads(f.read())
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)
    except:
        return None


SECRET_KEY = get_secret('SECRET_KEY')

# Facebook
# snucoffee계정
APP_ID = get_secret('FACEBOOK_APP_ID')
APP_SECRET = get_secret('FACEBOOK_APP_SECRET')
# FIXME: 이 그룹은 현재 snucoffee계정이 가입한 django_test 그룹이다.
FACEBOOK_GROUP_ID = '542458402875116'  # django_test
# FIXME: 이 토큰은 2개월후 만료된다.
FACEBOOK_TOKEN = get_secret('FACEBOOK_APP_TOKEN_60')

# Naver Map
NAVER_CLIENT_ID = get_secret("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = get_secret("NAVER_CLIENT_SECRET")

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'caffein',
        'USER': 'postgres',
        'PASSWORD': '0814',
        'HOST': 'db',
        'PORT': '5432',
    }
}
# DEBUG toolbar
INTERNAL_IPS = ('127.0.0.1',)

# EMAIL provider
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = ['*']
