from django.urls import path
from .user_management_views import *

urlpatterns = [
    path('getalluser', GetAllUsersView.as_view()),
    path('edituserform/<int:pk>', EditUserFormView.as_view()),
    path('add_user_page/add_user/', AddUserFormView.as_view()),
    path('add_user_page/', AddUserPageFormView.as_view()),
    path('permission',GetPermissions.as_view())
]