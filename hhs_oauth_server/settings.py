"""
Django settings for hhs_oauth_server project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.contrib.messages import constants as messages
from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cakehme*+^#hylq8uz2eszps%o!5!+*#1@+*83gmp$o(u3%!ldp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrapform',
    #'localflavor',
    'apps.fhir',
    'apps.nppes_handler',
    'apps.signups',
    'apps.core',
    'apps.accounts',
    'apps.home',
    'apps.api',
    'apps.capabilities',
    'apps.dot_ext',
    'corsheaders',
    'pymongo',

    # DOT must be installed after apps.dot_ext in order to override templates
    'oauth2_provider',
    'debug_toolbar',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)
CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'hhs_oauth_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                 os.path.join(BASE_DIR, 'templates'),
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

WSGI_APPLICATION = 'hhs_oauth_server.wsgi.application'


MESSAGE_TAGS ={ messages.DEBUG:   'debug',
                messages.INFO:    'info',
                messages.SUCCESS: 'success',
                messages.WARNING: 'warning',
                messages.ERROR:   'danger'
                }




# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'collectedstatic')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'sitestatic'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s [%(process)d] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'hhs_server': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'oauth2_provider': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'oauthlib': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

#Email Sending Opts
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
HOSTNAME_URL = "https://oauth.npi.io"
SEND_EMAIL= True
ORGANIZATION_NAME = "oAuth2"
EMAIL_BACKEND = 'django_ses.SESBackend'
SIGNUP_TIMEOUT_DAYS = 3
EMAIL_HOST_USER = 'sales@videntity.com'
INVITE_REQUEST_ADMIN = 'sales@videntity.com'

MIN_PASSWORD_LEN = 8
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            )

OAUTH2_PROVIDER_APPLICATION_MODEL='dot_ext.Application'
OAUTH2_PROVIDER = {
    'OAUTH2_VALIDATOR_CLASS': 'apps.dot_ext.oauth2_validators.SingleAccessTokenValidator',
    'OAUTH2_SERVER_CLASS': 'apps.dot_ext.oauth2_server.Server',
    'SCOPES_BACKEND_CLASS': 'apps.dot_ext.scopes.CapabilitiesScopes',
}

# These choices will be available in the expires_in field
# of the oauth2 authorization page.
DOT_EXPIRES_IN = (
    (86400, _("1 Day")),
    (86400*7, _("1 Week")),
    (86400*365, _("1 Year")),
    (86400*365*100, _("Forever")),
)

try:
    from settings_local import *
except:
    pass
