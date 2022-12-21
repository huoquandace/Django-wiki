from django.urls import path

from ts.views import *


urlpatterns = [
    path('', Ts.as_view() ,name=''),
    path('ts1/', Ts1.as_view() ,name='ts1'),
]
