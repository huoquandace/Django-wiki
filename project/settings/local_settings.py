from pathlib import Path

from settings.base import INSTALLED_APPS

SECRET_KEY = 'dovanthanh'

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

import os, sys
sys.path.insert(0, os.path.join(Path(__file__).resolve().parent.parent, 'apps')) # Change Project root

INSTALLED_APPS += [
    'core.apps.CoreConfig',
    'authentication.apps.AuthenticationConfig',
]

AUTH_USER_MODEL = 'authentication.User'

AUTH_PASSWORD_VALIDATORS =[]