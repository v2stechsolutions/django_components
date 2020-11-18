from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (LoginView, LogoutView, 
                    Dashboard, GendocxView, 
                    CustomTokenObtainPairView, NewPasswordView, 
                    GetLabels, GetLangauges, CustomTokenRefreshView,
                    GetToast)

app_name = "user_authentication"

urlpatterns = [
    path('api/rest-auth/', include('rest_auth.urls')),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name = "logout"),
    path('dashboard/', Dashboard.as_view(), name="dashboard"),
    path('download/',GendocxView.as_view(), name='download'),
    path('access_token/', CustomTokenObtainPairView.as_view(), name="gettoken"),
    # path('refresh_token/', TokenRefreshView.as_view()),
    path('refresh_token/', CustomTokenRefreshView.as_view()),
    path('forgot_password/', NewPasswordView.as_view(), name="forgot_password"),
    path('get_labels/', GetLabels.as_view(), name="get_labels"),
    path('get_languages/', GetLangauges.as_view(), name="get_labels"),
    path('toast_msg/', GetToast.as_view(), name="set_language")
    # path('dashboard/get_nav_labels/', GetNavLabels.as_view(), name="get_nav_labels"),
]
