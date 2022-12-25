from django.urls import path


from authentication.views.ver_1 import (
    Index,
    ImportUser,
    DowloadUserCsvTemplate
)

urlpatterns = [
    path('', Index.as_view(), name=''),
    path('user_add_csv/', ImportUser.as_view(), name='user_add_csv'),
    path('user_add_csv/download_template/', DowloadUserCsvTemplate.as_view(), name='download'),
]