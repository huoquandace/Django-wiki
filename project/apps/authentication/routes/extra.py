from django.urls import path


from authentication.views.extra import (
    ProfileView,
    ProfileUpdateView,
    UserDetail,
    UserList,
    UserAddCsv,
    DowloadUserCsvTemplate,
    UserListToPdf,
)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name='profile_update'),
    path('user/<int:pk>/', UserDetail.as_view(), name='profile_detail'),
    path('user/list/', UserList.as_view(), name='user_list'),
    path('user/list/to_pdf/', UserListToPdf.as_view(), name='user_list_to_pdf'), 
    path('user/add/', UserAddCsv.as_view(), name='user_add_csv'),
    path('user/add/csv/', UserAddCsv.as_view(), name='user_add_csv'),
    path('user/add/csv/download_template/', DowloadUserCsvTemplate.as_view(), name='download'),
]