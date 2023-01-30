from django.urls import path

from authentication.views.base import *


urlpatterns = [
    path('', AuthIndex.as_view() ,name='auth_index'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('register/', Register.as_view(), name='register'),
    path('register/done/', RegisterDone.as_view(), name='register_done'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileView.as_view(), name='profile_update'), # not yet

    path('user/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('user/list/', UserList.as_view(), name='user_list'),
    path('user/add/', UserAdd.as_view(), name='user_add'),
    path('user/add/by_info/', UserAddByInfo.as_view(), name='user_add_by_info'),
    path('user/update/<int:pk>/', UserDetail.as_view(), name='user_update'), # not yet
]