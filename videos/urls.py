from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/requests/', views.VideoGenerationRequestListCreateAPIView.as_view(), 
         name='video-request-list-create'),
    path('api/v1/requests/<int:request_id>/', views.VideoGenerationRequestDetailAPIView.as_view(), 
         name='video-request-detail'),
    path('api/v1/requests/<int:request_id>/status/', views.VideoGenerationStatusAPIView.as_view(), 
         name='video-request-status'),
    path('api/v1/requests/<int:request_id>/regenerate/', views.RegenerateVideoAPIView.as_view(), 
         name='video-regenerate'),

     # Template views
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('demo/', views.DemoView.as_view(), name='demo'),
]