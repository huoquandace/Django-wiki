import os, sys
from pathlib import Path

from settings.base import INSTALLED_APPS, TEMPLATES, BASE_DIR

SECRET_KEY = 'dovanthanh'

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

sys.path.insert(0, os.path.join(BASE_DIR, 'apps')) # Change Project root

INSTALLED_APPS += [
    'core.apps.CoreConfig',
    'authentication.apps.AuthenticationConfig',
    'ts.apps.TsConfig',
]

AUTH_USER_MODEL = 'authentication.User'

AUTH_PASSWORD_VALIDATORS =[]

TEMPLATES[0]['DIRS'] = [os.path.join(BASE_DIR, 'templates')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/auth/profile/'
LOGOUT_REDIRECT_URL = '/auth/login/'

# Fixes django generic view LoginView authentication error when user is_active = False
AUTHENTICATION_BACKENDS = [
    'authentication.backend.CustomModelBackend',
]

# Send email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / 'emails'