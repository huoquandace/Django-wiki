import os, sys
from pathlib import Path

SECRET_KEY = 'key'
DEBUG = True
ALLOWED_HOSTS =[]

INSTALLED_APPS = [
    # 'django.contrib.admin', # Admin site apps
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions', # Sessions app 
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True, # Must be enabled to request to admin page
        # 'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                # 'django.template.context_processors.debug',
                # 'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                # 'django.contrib.messages.context_processors.messages',
            ]
        }
    }
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

STATIC_URL = 'static/'

WSGI_APPLICATION = 'wsgi.application'

ROOT_URLCONF = 'urls' # Project url root

sys.path.insert(0, os.path.join(Path(__file__).resolve().parent, 'apps')) # Change Project root

SILENCED_SYSTEM_CHECKS = ["admin.W411"] # Turn off warning messages