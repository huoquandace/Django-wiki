from django.urls import path


from authentication.views.ver_1 import (
    Profile,
    UserList,
    ImportUser,
    DowloadUserCsvTemplate,
    UserListToPdf,
)

urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('user_list/', UserList.as_view(), name='user_list'),
    path('user_list/to_pdf/', UserListToPdf.as_view(), name='user_list_to_pdf'), 
    path('user_add_csv/', ImportUser.as_view(), name='user_add_csv'),
    path('user_add_csv/download_template/', DowloadUserCsvTemplate.as_view(), name='download'),
]