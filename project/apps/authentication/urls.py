from django.urls import path

from authentication.views import *


urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),

    path('password_change/done/', Logout.as_view(), name='password_change_done'),
    path('password_reset/', Logout.as_view(), name='password_reset'),
    path('password_reset/done/', Logout.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', Logout.as_view(), name='password_reset_confirm'),
    path('reset/done/', Logout.as_view(), name='password_reset_complete'),

    path('profile/', Profile.as_view(), name='profile'),
    path('register/', Register.as_view(), name='register'),
    path('register/done/', RegisterDone.as_view(), name='register_done'),
]
