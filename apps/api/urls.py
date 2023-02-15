from django.urls import path, include


urlpatterns = [
    path('users/', include('api.routes.api_urls')),
    path('test/', include('api.routes.test_urls')),
]