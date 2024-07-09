import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideoSerializer, TextSerializer
from emoji import emojize
import threading
from django.http import FileResponse
from .utils import process_video
from .models import ProcessingTasks


class UploadVideoView(generics.CreateAPIView):
    serializer_class = VideoSerializer

    def post(self, request, *args, **kwargs):
        file_serializer = VideoSerializer(data=request.data)
        if file_serializer.is_valid():
            instance = file_serializer.save()
            video_name = instance.file.name.split("/")[-1]
            return Response({"video_name": video_name}, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddTextToVideoView(generics.CreateAPIView):
    serializer_class = TextSerializer

    def post(self, request, *args, **kwargs):
        text_serializer = TextSerializer(data=request.data)
        if text_serializer.is_valid():
            video_path = os.path.join(
                settings.MEDIA_ROOT,
                "videos",
                text_serializer.validated_data["video_name"],
            )
            task_id = ProcessingTasks.objects.create(video_path=video_path).uid

            new_video_name = f"edited_{task_id}.mp4"
            output_path = os.path.join(settings.MEDIA_ROOT, "videos", new_video_name)
            text = emojize(text_serializer.validated_data["text"])
            x = text_serializer.validated_data["x"]
            y = text_serializer.validated_data["y"]
            t = text_serializer.validated_data["t"]
            d = text_serializer.validated_data["d"]
            s = text_serializer.validated_data["s"]

            # Start the video processing in a background thread
            threading.Thread(
                target=process_video,
                args=(task_id, video_path, output_path, text, x, y, t, d, s),
            ).start()

            # Return a response immediately
            return Response(
                {"task_id": task_id, "new_video_name": new_video_name},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(text_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DownloadVideoView(APIView):
    def get(self, request, task_id, *args, **kwargs):
        try:
            task = ProcessingTasks.objects.get(uid=task_id)
            video_path = task.video_path
        except ProcessingTasks.DoesNotExist:
            return Response(
                {"error": "Processing task not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if task.status == "processing":
            return Response(
                {"error": "Video is still processing"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif task.status == "failed":
            return Response(
                {"error": "Processing failed"}, status=status.HTTP_400_BAD_REQUEST
            )

        if os.path.exists(video_path):
            return FileResponse(
                open(video_path, "rb"),
                content_type="video/mp4",
                as_attachment=True,
                filename=f"edited_{task_id}.mp4",
            )
        else:
            return Response({"error": "Video not found"}, status=status.HTTP_404_NOT)
