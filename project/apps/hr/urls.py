from django.urls import path

from hr.views import *


urlpatterns = [
    path('list/', UserList.as_view(), name='user_list'),
]
