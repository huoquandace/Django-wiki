from django.urls import path


from authentication.views.v1 import (
    ProfileView,
    UserSettings,
    UserList,
    ImportUser,
    DowloadUserCsvTemplate,
    UserListToPdf,
)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>/', UserSettings.as_view(), name='profile_update'),
    path('user_list/', UserList.as_view(), name='user_list'),
    path('user_list/to_pdf/', UserListToPdf.as_view(), name='user_list_to_pdf'), 
    path('user_add_csv/', ImportUser.as_view(), name='user_add_csv'),
    path('user_add_csv/download_template/', DowloadUserCsvTemplate.as_view(), name='download'),
]