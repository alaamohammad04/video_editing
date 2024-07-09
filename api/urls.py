from django.urls import path
from .views import UploadVideoView, AddTextToVideoView, DownloadVideoView

urlpatterns = [
    path("upload/", UploadVideoView.as_view(), name="upload_video"),
    path("add-text/", AddTextToVideoView.as_view(), name="add_text_to_video"),
    path(
        "download/<uuid:task_id>/", DownloadVideoView.as_view(), name="download_video"
    ),
]
