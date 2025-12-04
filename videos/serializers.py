from rest_framework import serializers
from .models import VideoGenerationRequest

class VideoGenerationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGenerationRequest
        fields = '__all__'
        read_only_fields = ['id', 'status', 'video_url', 'video_file', 'error_message', 'created_at', 'updated_at']

class TextToVideoSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True, max_length=1000)
    location = serializers.CharField(required=False, max_length=255, allow_blank=True)
    aspect_ratio = serializers.CharField(required=False, default='16:9')
    resolution = serializers.CharField(required=False, default='720p')
    negative_prompt = serializers.CharField(required=False, allow_blank=True)

class ImageToVideoSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True, max_length=1000)
    store_image = serializers.ImageField(required=True)
    location = serializers.CharField(required=False, max_length=255, allow_blank=True)
    aspect_ratio = serializers.CharField(required=False, default='16:9')
    resolution = serializers.CharField(required=False, default='720p')
    negative_prompt = serializers.CharField(required=False, allow_blank=True)

class VideoStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGenerationRequest
        fields = ['id', 'status', 'video_url', 'video_file', 'error_message', 'created_at', 'updated_at']
        read_only_fields = fields