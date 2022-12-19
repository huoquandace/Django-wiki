from django.urls import path

from authentication.views import *


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('profile/', Profile.as_view(), name='profile'),
]
