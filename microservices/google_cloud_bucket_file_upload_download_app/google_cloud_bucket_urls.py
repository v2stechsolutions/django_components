from django.urls import path
from .google_cloud_bucket_views import *

urlpatterns = [
    path('', GoogleCloudHomeView.as_view()),
    path('filelist', CloudBucketFileListView.as_view()),
    path('upload', CloudBucketFileUpload.as_view()),
    path('download', CloudBucketFileDownload.as_view())
]