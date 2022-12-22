from django.urls import path


from authentication.views.user_management_v1 import (
    Index,
)

urlpatterns = [
    path('', Index.as_view(), name=''),
]