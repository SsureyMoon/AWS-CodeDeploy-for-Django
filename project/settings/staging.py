from .base import *


env = os.environ.get

SECRET_KEY = env('SECRET_KEY')

DEBUG = False

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME = env('S3_BUCKET_NAME')

MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
del STATIC_ROOT
del STATICFILES_FINDERS
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME': env('PSQL_DB_NAME'),
        'USER': env('PSQL_DB_USER'),
        'PASSWORD': env('PSQL_DB_PASSWD'),
        'HOST': env('PSQL_HOST'),
        'PORT': env('PSQL_PORT'),
    }
}

LOG = path.join(LOG_DIR, 'django_app.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG,
            'formatter': 'default',
        },
    },

    # Loggers
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

JWT_AUTH = {
    'JWT_SECRET_KEY': env('JWT_SECRET_KEY')
}
