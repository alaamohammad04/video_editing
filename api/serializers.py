from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class TextSerializer(serializers.Serializer):
    video_name = serializers.CharField(
        help_text="Name of the video file that you get from the upload API"
    )
    text = serializers.CharField(help_text="Text to be added")
    x = serializers.IntegerField(help_text="X-coordinate of the text")
    y = serializers.IntegerField(help_text="Y-coordinate of the text")
    t = serializers.FloatField(help_text="Start time of the text")
    d = serializers.FloatField(help_text="End time of the text")
    s = serializers.IntegerField(help_text="Font size of the text")
