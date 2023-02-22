from django.urls import path, include

from accounts.views.base import *


urlpatterns = [
    path('', AuthIndex.as_view() ,name='auth_index'),
    path('auth/', include('accounts.routes.auth')),
    path('account/', include('accounts.routes.account')),
    path('user_manager/', include('accounts.routes.user_manager')),
]
