from django.urls import path
from . import views

urlpatterns = [
    path('text-to-video/', views.TextToVideoAPIView.as_view(), name='text-to-video'),
    path('image-to-video/', views.ImageToVideoAPIView.as_view(), name='image-to-video'),
    path('videos/', views.VideoListAPIView.as_view(), name='video-list'),
    path('videos/<int:video_id>/', views.VideoDetailAPIView.as_view(), name='video-detail'),
    path('videos/<int:video_id>/status/', views.VideoStatusAPIView.as_view(), name='video-status'),
    path('videos/<int:video_id>/regenerate/', views.RegenerateVideoAPIView.as_view(), name='regenerate-video'),

]