import os, sys
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from settings.base import INSTALLED_APPS, TEMPLATES, BASE_DIR, MIDDLEWARE

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




LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('es', _('Spanish')),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

MIDDLEWARE += [
    'django.middleware.locale.LocaleMiddleware',
]