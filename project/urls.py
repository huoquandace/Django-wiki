from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns (
    path('', include('core.urls')),
    path('ts/', include('ts.urls')),
    path('auth/', include('authentication.routes.urls')),
    path('auth_v1/', include('authentication.routes.user_management_v1')),
    path('hr/', include('hr.urls')),

    prefix_default_language=False
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)