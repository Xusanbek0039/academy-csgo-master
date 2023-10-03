from pathlib import Path
import dotenv
import os

dotenv.load_dotenv()
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-4q9gp)oo$8les8%*3#bl^w_h=-w0g4i%y0!3iepn6-_qyl5z1sasdgdsgadsgadsgerjhg244'

FERNET_KEY = b'MANA SHU TASODIFY KALIT'


DEBUG = int(os.environ.get('DEBUG_VALUE', 0))
ALLOWED_HOSTS = ['*']

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

AUTH_USER_MODEL = 'steam.User'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.steam.SteamOpenId',
    'django.contrib.auth.backends.ModelBackend',
)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    #Thirdparty
    'crispy_forms',
    'social_django',
    'django_filters',
    'debug_toolbar',

    # my apps
    'steam',
    'store.apps.StoreConfig',
    'stats.apps.StatsConfig',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'csgo.urls'

STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'stats.context_processors.get_server'
            ],
        },
    },
]

WSGI_APPLICATION = 'csgo.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'CHARSET': 'utf8', # Bu satrni olib tashlang
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

TIME_ZONE = 'UTC'

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static_root')

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR,'uploads')

LOGIN_REDIRECT_URL = 'stats:index'

SOCIAL_AUTH_STEAM_API_KEY = os.environ.get('STEAM_API_KEY')
SOCIAL_AUTH_STEAM_EXTRA_DATA = ['player']
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = ('social_core.backends.steam.SteamOpenId',)

STEAM_WEB_API_KEY = os.environ.get('STEAM_API_KEY')
CRISPY_TEMPLATE_PACK = 'bootstrap4' 


KHALTI_VERIFICATION_URL = 'https://khalti.com/api/v2/payment/verify/'

REPORT_DISCORD_WEBHOOK_URL = os.environ.get('REPORT_DISCORD_WEBHOOK_URL')
APPEAL_DISCORD_WEBHOOK_URL = os.environ.get('APPEAL_DISCORD_WEBHOOK_URL')
CONTACT_DISCORD_WEBHOOK_URL = os.environ.get('CONTACT_DISCORD_WEBHOOK_URL')

ADMINS = [(os.environ.get('ADMIN_ONE_NAME'),os.environ.get('ADMIN_ONE_EMAIL'),)]
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True
SERVER_EMAIL = os.environ.get('SERVER_EMAIL')

SITE_URL = os.environ.get("SITE_URL","http://127.0.0.1:8000")

STRIPE_SK=os.environ.get("STRIPE_SK")
STRIPE_WH_SECRET = os.environ.get("STRIPE_WH_SECRET")

KHALTI_API_SECRET_KEY = os.environ.get('KHALTI_API_SECRET_KEY')

# For Django Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN",""),
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.5,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)