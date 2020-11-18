from django.conf.urls import url
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .user_and_role_management_views import *

urlpatterns = [
    path('user', UserView.as_view()),
    path('user/<int:pk>', UserIdBasedView.as_view()),
    path('role',RoleView.as_view()),
    path('role/<int:pk>',RoleIdBasedView.as_view()),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]