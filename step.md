# Development steps

## 1. Initialize

### 1.1 Start project

Enter this code into command line to create django project folder

&nbsp;&nbsp; `django-admin startproject wiki`

### 1.2 Rebuild project structure layout

- change name wiki->settings, settings->base
- move urls asgi wsgi to root Directory and edit DJANGO_SETTINGS_MODULE to settings.base
- config:   ROOT_URLCONF = 'urls'
  WSGI_APPLICATION = 'wsgi.application'
- create folder apps and add to settings: sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

## 2.

## 3.

## 4.

- create folder template and edit: settings -> TEMPLATES: 'DIRS': [os.path.join(BASE_DIR, 'templates'),],
- create folder static and add to settings:     STATIC_URL = 'static/'
  STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
- create folder media and add to settings:  MEDIA_URL = '/media/'
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
- add to urls:  from django.conf import settings
  from django.conf.urls.static import static
  ...
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
- create folder locale/[lang_code]/LC_MESSAGES and add to settings:     USE_I18N = True
  LANGUAGE_CODE = 'en'
  LOCALE_PATHS = [BASE_DIR / 'locale/',]
  MIDDLEWARE += ['django.middleware.locale.LocaleMiddleware',]
  LANGUAGES = (
  ('en', _('English')),
  ('vi', _('Vietnamese')),
  ('ja', _('Japanese')),
  )
- add to urls:  from django.urls import path, include
  from django.conf.urls.i18n import i18n_patterns
  ...
  urlpatterns += i18n_patterns (
  path('auth/', include('authentication.routes.base')),
  
  # prefix_default_language=False
  
  )
- create .gitignore

