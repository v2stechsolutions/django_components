from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='REST APIS')

urlpatterns = [
    path('swagger',schema_view),
    path('admin/', admin.site.urls),
    path('drive/', include('google_drive_file_upload_download_app.google_drive_urls')),
    path('management/', include('user_and_role_management_with_jwt_token_authentication_app.user_and_role_management_urls')),
    path('cloud/', include('google_cloud_bucket_file_upload_download_app.google_cloud_bucket_urls')),
    path('', include('django.contrib.auth.urls')),
    path('jwt/', include('jwt_based_authentication.urls')),
    path('session/', include('session_based_authentication.urls')),
    path('redis/', include('django_redis_caching.urls')),
    path('mongo/', include('restapi_using_mongodb.urls')),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

  