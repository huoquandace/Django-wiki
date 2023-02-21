# Development steps

## 1. Initialize

### 1.1 Start project

Enter this code into command line to create django project folder:
  ```
  django-admin startproject wiki
  ```

### 1.2 Rebuild project structure layout

- Rename folder `wiki` to `settings`, file `settings.py` to `base.py`
- Move files `urls.py` `asgi.py` `wsgi.py` to root directory and change:
  ```
  import os, sys
  ...
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')
  ```

- Open `setings/base.py` and change:
  ```
  ROOT_URLCONF = 'urls'
  WSGI_APPLICATION = 'wsgi.application'
  ```

### 1.3 Initial settings

#### 1.3.1 Git settings
- Create `.gitignore`:
  ```
  __pycache__
  db.sqlite3
  ```

#### 1.3.2 Create folder contains project apps
- Create folder `apps` and add to `setings/base.py`:
  ```
  sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
  ```
#### 1.3.3 Create folder contains templates
- Create folder `templates` and edit `setings/base.py`:
  ```
  TEMPLATES = [
    {
      ...
      'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
      ...
    },
  ]
  ```
#### 1.3.4 Setting for static and media files
- Create folder `static` and add to `setings/base.py`:
  ```
  STATIC_URL = 'static/'
  STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
  ```
- Create folder `media` and add to `setings/base.py`:
  ```
  MEDIA_URL = '/media/'
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  ```
- Customize `urls.py`:  
  ```
  from django.conf import settings
  from django.conf.urls.static import static
  ...
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  ```

#### 1.3.5 Multiple languages settings
- Create folders `locale/[lang_code]/LC_MESSAGES` and add to `settings/base.py`:
  ```
  from django.utils.translation import gettext_lazy as _
  ...
  USE_I18N = True
  LANGUAGE_CODE = 'en'
  LOCALE_PATHS = [BASE_DIR / 'locale/',]
  LANGUAGES = (
    ('en', _('English')),
    ('vi', _('Vietnamese')),
    ('ja', _('Japanese')),
  )
  ```
- Add middleware bettween session and common:
  ```
  MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
  ]
  ```

- Customize `urls.py`:
  ```
  from django.urls import path, include
  from django.conf.urls.i18n import i18n_patterns
  ...
  urlpatterns += i18n_patterns (

    # prefix_default_language=False
  )
  ```

- Make file .po and compile to .mo by code:
  ```
  django-admin makemessages --all --ignore=env
  django-admin compilemessages --ignore=env
  ```

- Ignore files `.mo` by add to `.gitignore` :
  ```
  *.mo
  ```
## 2.

## 3.

## 4.

- create .gitignore
