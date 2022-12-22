from django.urls import path


from authentication.views.user_management_v1 import (
    Index,
    userdata
)

urlpatterns = [
    path('', Index.as_view(), name=''),
    # path('user_add_csv/', userdata, name='user_add_csv'),
]