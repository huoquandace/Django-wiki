from django.urls import path

from api.views import *


urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user_list_create_api'),
    # path('user/<int:pk>/', ),
]