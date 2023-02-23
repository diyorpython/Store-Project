from pathlib import Path
import environs
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

env = environs.Env()
environs.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!)m96pr=(xujfgzmx*9h7p0k0$b8rr^a))za(q)4-p2ybms**d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # External apps
    "crispy_forms",
    "rosetta",
    "crispy_bootstrap5",
    'django_q',
    "rest_framework",
    'rest_framework.authtoken',
    # my apps
    'core.apps.CoreConfig',
    'api.apps.ApiConfig'
]

AUTH_USER_MODEL = 'core.Customuser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR/"templates"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': env.str('ENGINE'),
#         'NAME': env.str('NAME'),
#         'USER': env.str('USER'),
#         'PASSWORD': env.str('PASSWORD'),
#         'HOST': env.str('HOST'),
#         'PORT': env.str('PORT')
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3", # This is where you put the name of the db file. 
                 # If one doesn't exist, it will be created at migration time.
    }
}


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': [
        'apps.core.pagination.StandardResultsSetPagination'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('uz', _('Uzbek'))
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = "media/"
MEDIA_ROOT = "media"

LOGIN_URL ='/login/'
LOGIN_REDIRECT_URL ='/login/'
LOGOUT_REDIRECT_URL = '/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MODELTRANSLATION_DEFAULT_LANGUAGE = "en"

# Message tags
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # new
SITE_ID = 1 # new
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'dbaxtiyorov35@gmail.com'
EMAIL_HOST_PASSWORD = 'rujgcbrwwbjgnesw'

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 2,  # The number of workers to use in the cluster.
    'timeout': 300,  # The number of seconds a worker is allowed to spend on a task before it’s terminated.
    'retry': 300,  # The number of seconds a broker will wait for a cluster to finish a task,
                   # before it’s presented again.
    'save_limit': 0,  # Limits the amount of successful tasks saved to Django. Set to 0 for unlimited.
    'queue_limit': 50,  # This does not limit the amount of tasks that can be queued on the broker,
                        # but rather how many tasks are kept in memory by a single cluster.
    'bulk': 10,  # Sets the number of messages each cluster tries to get from the broker per call.
    'orm': 'default',
    "max_attempts": 1  # Limit the number of retry attempts for failed tasks
}
