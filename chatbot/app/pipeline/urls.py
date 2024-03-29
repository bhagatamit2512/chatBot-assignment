from django.urls import path
from pipeline.views.uploaded_file import UploadedFileView
urlpatterns = [
    path(
        "files/",
        UploadedFileView.as_view(),
        name="uploaded_file",
    ),
 ]