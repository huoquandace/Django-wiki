from django.urls import path

from ts.views import *


urlpatterns = [
    path('', Ts.as_view() ,name=''),
]
