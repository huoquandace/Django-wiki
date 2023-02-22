from django.urls import path

from accounts.views.base import *


urlpatterns = [
    path('user/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('user/list/', UserList.as_view(), name='user_list'),
    path('user/list/to_pdf/', UserListToPdf.as_view(), name='user_list_to_pdf'), 
    path('user/add/', UserAdd.as_view(), name='user_add'),
    path('user/add/by_info/', UserAddByInfo.as_view(), name='user_add_by_info'),
    path('user/add/by_csv/', UserAddByCsv.as_view(), name='user_add_by_csv'),
    path('user/add/by_csv/download_template/', DowloadUserCsvTemplate.as_view(), name='user_template_csv_download'),
    path('user/edit/<int:pk>/', UserEdit.as_view(), name='user_edit'),
    path('user/delete/<int:pk>/', UserDelete.as_view(), name='user_delete'),
    
    path('user/group/list/', UserGroupList.as_view(), name='user_group_list'),
    path('user/group/add/', UserGroupAdd.as_view(), name='user_group_add'),
]
