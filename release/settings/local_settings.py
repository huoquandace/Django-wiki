import os, sys
from django.utils.translation import gettext_lazy as _
from settings.base import INSTALLED_APPS, TEMPLATES, BASE_DIR, MIDDLEWARE


INSTALLED_APPS += ['authentication',]
sys.path.insert(0, os.path.join(BASE_DIR, 'apps')) # Change App root
AUTH_USER_MODEL = 'authentication.User'
AUTH_PASSWORD_VALIDATORS =[]
TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'templates')]
# Settings
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0', ]
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
# Media & Static
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
# Auth redirect
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/auth/profile/'
LOGOUT_REDIRECT_URL = '/auth/login/'
# Fixes django generic view LoginView authentication error when user is_active = False
AUTHENTICATION_BACKENDS = ['authentication.backend.CustomModelBackend',]
# Send email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / 'emails'
# Language settings
LANGUAGE_CODE = 'en'
USE_L10N = True
LANGUAGES = (('en', _('English')), ('vi', _('Vietnam')),)
LOCALE_PATHS = [BASE_DIR / 'locale/',]
MIDDLEWARE += ['django.middleware.locale.LocaleMiddleware',]
