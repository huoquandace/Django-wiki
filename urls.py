from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/', include('api.urls')),
    path('ts/', include('ts.urls')),
]

urlpatterns += i18n_patterns (
    path('auth/', include('authentication.routes.base')),

    # prefix_default_language=False
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)