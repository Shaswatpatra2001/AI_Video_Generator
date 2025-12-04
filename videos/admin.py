from django.contrib import admin
from .models import VideoGenerationRequest

@admin.register(VideoGenerationRequest)
class VideoGenerationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'prompt', 'status', 'created_at']
    list_filter = ['status', 'created_at'] 
    search_fields = ['prompt', 'location', 'error_message']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Input Data', {
            'fields': ('prompt', 'store_image', 'product_image', 'location')
        }),
        ('Video Settings', {
            'fields': ('aspect_ratio', 'resolution', 'negative_prompt')
        }),
        ('Generation Results', {
            'fields': ('status', 'video_url', 'video_file', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )