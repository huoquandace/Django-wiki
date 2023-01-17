from django.urls import path

from authentication.views.extra import *


urlpatterns = [
    path('', AuthExtra.as_view() ,name='auth_extra'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('user/add/', UserAdd.as_view(), name='user_add'),
    path('user/list/', UserList.as_view(), name='user_list'),
    path('user/edit/<int:pk>/', UserList.as_view(), name='user_edit'),
    path('user/delete/<int:pk>/', UserDelete.as_view(), name='user_delete'),
    # path('user/list/to_pdf/', UserListToPdf.as_view(), name='user_list_to_pdf'), 
    # path('user/add/csv/', UserAddCsv.as_view(), name='user_add_csv'),
    # path('user/add/csv/download_template/', DowloadUserCsvTemplate.as_view(), name='download'),
]