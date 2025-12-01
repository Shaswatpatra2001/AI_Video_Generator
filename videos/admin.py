from django.contrib import admin
from .models import VideoGenerationRequest

@admin.register(VideoGenerationRequest)
class VideoGenerationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'location', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['location', 'offer_text']
    readonly_fields = ['created_at', 'updated_at']