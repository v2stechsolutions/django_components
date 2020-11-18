from django.urls import path
from django.conf.urls import url
from .import user_registration_views as views
from .user_registration_views import(
    CheckEmail, CheckUsername, RegistrationFormView,
    GetQualificationDropDown, GetRoleDropDown)

urlpatterns = [
    path('check_username/', CheckUsername.as_view()),
    path('check_email/', CheckEmail.as_view()),
    path('register/', RegistrationFormView.as_view()),
    path('get_qualification/', GetQualificationDropDown().as_view()),
    path('get_roles/', GetRoleDropDown().as_view())
]