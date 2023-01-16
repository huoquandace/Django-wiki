from django.urls import path


from authentication.views.extra import (
    AuthExtra,
    ProfileView, ProfileUpdateView, ProfileUpdateView2,
    UserDetail, UserList, UserAdd,
    UserAddCsv, DowloadUserCsvTemplate,
    UserListToPdf,
)

urlpatterns = [
    path('', AuthExtra.as_view() ,name='auth_extra'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/update2/', ProfileUpdateView2.as_view(), name='profile_update2'),
    path('user/<int:pk>/', UserDetail.as_view(), name='profile_detail'),
    path('user/list/', UserList.as_view(), name='user_list'),
    path('user/list/to_pdf/', UserListToPdf.as_view(), name='user_list_to_pdf'), 
    path('user/add/', UserAdd.as_view(), name='user_add'),
    path('user/add/csv/', UserAddCsv.as_view(), name='user_add_csv'),
    path('user/add/csv/download_template/', DowloadUserCsvTemplate.as_view(), name='download'),
]