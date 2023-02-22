from django.urls import path, include

from accounts.views.base import *


urlpatterns = [
    path('', AuthIndex.as_view() ,name='auth_index'),
    path('', include('accounts.routes.base')),
]
