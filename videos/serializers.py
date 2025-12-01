from rest_framework import serializers
from .models import VideoGenerationRequest

class VideoGenerationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGenerationRequest
        fields = [
            'id', 'store_image', 'product_image', 'offer_text', 
            'location', 'status', 'generated_video_url', 
            'error_message', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'status', 'generated_video_url', 
            'error_message', 'created_at', 'updated_at'
        ]

class VideoGenerationRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGenerationRequest
        fields = ['store_image', 'product_image', 'offer_text', 'location']

class VideoGenerationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGenerationRequest
        fields = ['id', 'status', 'generated_video_url', 'error_message', 'updated_at']
        read_only_fields = ['id', 'status', 'generated_video_url', 'error_message', 'updated_at']