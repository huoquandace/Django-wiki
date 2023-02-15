from django.urls import path

from api.views.api_views import *


urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='user_list_create_api'),
    # path('user/<int:pk>/', ),

]