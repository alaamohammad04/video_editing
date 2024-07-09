from django.db import models
import uuid


class Video(models.Model):
    file = models.FileField(upload_to="videos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


TASK_STATUSES = [
    ("processing", "Processing"),
    ("failed", "Failed"),
    ("Completed", "Completed"),
]


class ProcessingTasks(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    status = models.CharField(
        max_length=20, default="processing", choices=TASK_STATUSES
    )
    video_path = models.CharField(max_length=520)
