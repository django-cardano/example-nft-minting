import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_PATH = Path(__file__).resolve().parent
ROOT_PATH = PROJECT_PATH.parent

DATA_PATH = ROOT_PATH / 'data'
TEMPLATES_PATH = PROJECT_PATH / 'templates'

load_dotenv(ROOT_PATH / '.env')

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY")

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = ['localhost']

ADMINS = (
    ('admin', 'admin@example.com',),
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cardano',

    'app.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_PATH],
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


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATA_PATH / 'db.sqlite3',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_ROOT = PROJECT_PATH / 'media'
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

# ------------------------------------------------------------------------------
DJANGO_CARDANO = {
    'NETWORK': 'testnet',
    'TOKEN_DUST': 1650000,
}

DJANGO_CARDANO_MINTING_POLICY_MODEL = 'core.MintingPolicy'
DJANGO_CARDANO_TRANSACTION_MODEL = 'core.Transaction'
DJANGO_CARDANO_WALLET_MODEL = 'core.Wallet'
