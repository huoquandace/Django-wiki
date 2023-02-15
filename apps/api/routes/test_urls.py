from django.urls import path

from api.views.test_views import *


urlpatterns = [
    path('', UserListView.as_view(), name='u_list'),
]