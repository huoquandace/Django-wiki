from django.urls import path

from accounts.views.auth_view import Login, Logout

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
