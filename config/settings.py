import os
DEBUG = False

ALLOWED_HOSTS = ['*']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'widget_tweaks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'django.contrib.staticfiles',
    'django_boost',
    "user",
    'app',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',
]

SESSION_ENGINE= 'django.contrib.sessions.backends.cached_db'

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_boost.context_processors.user_agent', # django boost
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRESQL_NAME'],
        'USER': os.environ['POSTGRESQL_USER'],
        'PASSWORD': os.environ['POSTGRESQL_PASSWORD'],
        'HOST': os.environ['POSTGRESQL_HOST'],
        'PORT': os.environ['POSTGRESQL_PORT'],
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.MyUser'

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/login/"


from django.contrib import messages
MESSAGE_TAGS = {
    messages.ERROR: 'rounded-0 alert alert-danger',
    messages.WARNING: 'rounded-0 alert alert-warning',
    messages.SUCCESS: 'rounded-0 alert alert-success',
    messages.INFO: 'rounded-0 alert alert-info',
    messages.DEBUG: 'rounded-0 alert alert-secondary',
 }

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
DEBUG_PROPAGATE_EXCEPTIONS = True


try:
    from .local_settings import *
except ImportError:
    pass

if not DEBUG:
    print("Not Debug Mode!!")

    SECRET_KEY = os.getenv('SECRET_KEY', 'Optional default value')
    import django_heroku
    django_heroku.settings(locals(), staticfiles=False)

    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)
    AWS_S3_REGION_NAME = "ap-northeast-1"
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'
    MEDIA_URL = '/image/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'image')

    DEFAULT_FILE_STORAGE = 'config.backends.MediaStorage'
