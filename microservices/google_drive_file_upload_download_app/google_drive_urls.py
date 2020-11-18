from django.urls import path
from .google_drive_views import *

urlpatterns = [
    path('', GoogleDriveHomeView.as_view()),
    path('filelist', GoogleDriveFileListView.as_view()),
    path('upload', GoogleDriveFileUploadView.as_view()),
    path('download', GoogleDriveFileDownloadView.as_view())
]