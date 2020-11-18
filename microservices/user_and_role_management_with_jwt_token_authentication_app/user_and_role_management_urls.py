from django.conf.urls import url
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .user_and_role_management_views import *
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('',LoginView.as_view()),
    path('dashboard',login_required(DashboardView.as_view())),
    path('dashboardhtml', login_required(DashboardHtmlView.as_view())),
    path('userwebpage',login_required(UserwebpageView.as_view())),
    path('userwebpagehtml', login_required(UserwebpageHtmlView.as_view())),
    path('rolewebpage', login_required(RolewebpageView.as_view())),
    path('rolewebpagehtml',login_required(RolewebpageHtmlView.as_view())),
    path('user',login_required(UserView.as_view())),
    path('user/<int:pk>',login_required(UserIdBasedView.as_view())),
    path('role',login_required(RoleView.as_view())),
    path('role/<int:pk>',login_required(RoleIdBasedView.as_view())),
    path('login/', DjangoLoginView.as_view()),
    path('logout',login_required(DjangoLogoutView.as_view())),
    path('token/', MyTokenObtainPairView.as_view()),
    path('permission/',login_required(PermissionView.as_view())),
    path('permission/<int:pk>', login_required(PermissionIdView.as_view())),
    # path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]