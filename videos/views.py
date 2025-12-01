from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import threading

from .models import VideoGenerationRequest
from .serializers import (
    VideoGenerationRequestSerializer, 
    VideoGenerationRequestCreateSerializer,
    VideoGenerationStatusSerializer
)
from .services import VideoGenerationService
from django.shortcuts import render
from django.views import View



class VideoGenerationRequestListCreateAPIView(APIView):
    
    @swagger_auto_schema(
        operation_description="Get all video generation requests",
        responses={200: VideoGenerationRequestSerializer(many=True)}
    )
    def get(self, request):
        video_requests, error = VideoGenerationService.get_all_video_requests()
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = VideoGenerationRequestSerializer(video_requests, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Create a new video generation request",
        request_body=VideoGenerationRequestCreateSerializer,
        responses={201: VideoGenerationRequestSerializer}
    )
    def post(self, request):
        serializer = VideoGenerationRequestCreateSerializer(data=request.data)
        if serializer.is_valid():
            store_image = serializer.validated_data['store_image']
            product_image = serializer.validated_data.get('product_image')
            offer_text = serializer.validated_data['offer_text']
            location = serializer.validated_data['location']
            
            video_request, error = VideoGenerationService.create_video_generation_request(
                store_image, product_image, offer_text, location
            )
            
            if error:
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
            
            video_url, gen_error = VideoGenerationService.generate_ai_video(video_request)
            
            if video_url:
                VideoGenerationService.update_video_request_status(
                    video_request.id, 'completed', video_url=video_url
                )
            else:
                VideoGenerationService.update_video_request_status(
                    video_request.id, 'failed', error_message=gen_error
                )
            
            updated_request, _ = VideoGenerationService.get_video_request_by_id(video_request.id)
            serializer = VideoGenerationRequestSerializer(updated_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoGenerationRequestDetailAPIView(APIView):
    
    @swagger_auto_schema(
        operation_description="Get video generation request details by ID",
        responses={200: VideoGenerationRequestSerializer}
    )
    def get(self, request, request_id):
        video_request, error = VideoGenerationService.get_video_request_by_id(request_id)
        if error:
            return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VideoGenerationRequestSerializer(video_request)
        return Response(serializer.data)

class VideoGenerationStatusAPIView(APIView):
    
    @swagger_auto_schema(
        operation_description="Get video generation status by request ID",
        responses={200: VideoGenerationStatusSerializer}
    )
    def get(self, request, request_id):
        video_request, error = VideoGenerationService.get_video_request_by_id(request_id)
        if error:
            return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VideoGenerationStatusSerializer(video_request)
        return Response(serializer.data)

class RegenerateVideoAPIView(APIView):
    
    @swagger_auto_schema(
        operation_description="Regenerate video for existing request",
        responses={200: VideoGenerationRequestSerializer}
    )
    def post(self, request, request_id):
        video_request, error = VideoGenerationService.get_video_request_by_id(request_id)
        if error:
            return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
        
        video_url, gen_error = VideoGenerationService.generate_ai_video(video_request)
        
        if video_url:
            VideoGenerationService.update_video_request_status(
                video_request.id, 'completed', video_url=video_url
            )
        else:
            VideoGenerationService.update_video_request_status(
                video_request.id, 'failed', error_message=gen_error
            )
        
        updated_request, _ = VideoGenerationService.get_video_request_by_id(request_id)
        serializer = VideoGenerationRequestSerializer(updated_request)
        return Response(serializer.data)
    


class DemoView(View):
    def get(self, request):
        return render(request, 'demo.html')

class DashboardView(View):
    def get(self, request):
        video_requests, error = VideoGenerationService.get_all_video_requests()
        
        if error:
            video_requests = []
        
        context = {
            'videos': video_requests,
            'total_videos': len(video_requests),
            'completed_videos': len([v for v in video_requests if v.status == 'completed']),
            'processing_videos': len([v for v in video_requests if v.status == 'processing']),
            'failed_videos': len([v for v in video_requests if v.status == 'failed']),
        }
        return render(request, 'dashboard.html', context)