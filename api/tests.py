from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Video
from django.conf import settings


class VideoUploadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_upload_video(self):
        with open(f"{settings.BASE_DIR}/test/video.mp4", "rb") as video:
            response = self.client.post(
                "/api/upload/", {"file": video}, format="multipart"
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AddTextToVideoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.video = Video.objects.create(file=f"{settings.BASE_DIR}/test/video.mp4")

    def test_add_text_to_video(self):
        data = {
            "video_name": self.video.file.name,
            "text": "Hello, World! 😊",
            "x": 100,
            "y": 200,
            "t": 5,
            "d": 10,
            "s": 24,
        }
        response = self.client.post("/api/add-text/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
