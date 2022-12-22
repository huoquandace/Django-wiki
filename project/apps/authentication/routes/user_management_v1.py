from django.urls import path


from authentication.views.user_management_v1 import (
    Index,
    ImportUser,
    download
)

urlpatterns = [
    path('', Index.as_view(), name=''),
    path('user_add_csv/', ImportUser.as_view(), name='user_add_csv'),
    path('download/', download, name='download'),
]