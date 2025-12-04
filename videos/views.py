from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VideoGenerationRequest
from .serializers import (
    VideoGenerationRequestSerializer,
    TextToVideoSerializer,
    ImageToVideoSerializer,
    VideoStatusSerializer
)
from .services import VideoGenerationService

class TextToVideoAPIView(APIView):
    def post(self, request):
        serializer = TextToVideoSerializer(data=request.data)
        if serializer.is_valid():
            video_request = VideoGenerationRequest.objects.create(**serializer.validated_data)
            VideoGenerationService.generate_video_sync(video_request)
            serializer = VideoGenerationRequestSerializer(video_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageToVideoAPIView(APIView):
    def post(self, request):
        serializer = ImageToVideoSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data.copy()
            store_image = data.pop('store_image')
            video_request = VideoGenerationRequest.objects.create(**data, store_image=store_image)
            VideoGenerationService.generate_video_sync(video_request)
            serializer = VideoGenerationRequestSerializer(video_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoListAPIView(APIView):
    def get(self, request):
        videos = VideoGenerationRequest.objects.all().order_by('-created_at')
        serializer = VideoGenerationRequestSerializer(videos, many=True)
        return Response(serializer.data)

class VideoDetailAPIView(APIView):
    def get(self, request, video_id):
        try:
            video = VideoGenerationRequest.objects.get(id=video_id)
            serializer = VideoGenerationRequestSerializer(video)
            return Response(serializer.data)
        except VideoGenerationRequest.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

class VideoStatusAPIView(APIView):
    def get(self, request, video_id):
        try:
            video = VideoGenerationRequest.objects.get(id=video_id)
            serializer = VideoStatusSerializer(video)
            return Response(serializer.data)
        except VideoGenerationRequest.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)

class RegenerateVideoAPIView(APIView):
    def post(self, request, video_id):
        try:
            video = VideoGenerationRequest.objects.get(id=video_id)
            video.status = 'pending'
            video.video_url = None
            video.video_file = None
            video.error_message = None
            video.save()
            VideoGenerationService.generate_video_sync(video)
            serializer = VideoGenerationRequestSerializer(video)
            return Response(serializer.data)
        except VideoGenerationRequest.DoesNotExist:
            return Response({"error": "Video not found"}, status=404)