from django.urls import path

from api.views.api_views import *
from api.views.data_views import *


urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user_list_create_api'),
    # path('user/<int:pk>/', ),

    path('test/', UserListView.as_view(), name='u_list'),
]