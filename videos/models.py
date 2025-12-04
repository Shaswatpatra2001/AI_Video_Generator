from django.db import models

class VideoGenerationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    prompt = models.TextField()
    store_image = models.ImageField(upload_to='store_images/', null=True, blank=True)
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    
    # Video parameters
    aspect_ratio = models.CharField(max_length=20, default='16:9')
    resolution = models.CharField(max_length=20, default='720p')
    negative_prompt = models.TextField(blank=True)
    
    # Generation results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    video_url = models.URLField(null=True, blank=True)
    video_file = models.FileField(upload_to='generated_videos/', null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Video #{self.id} - {self.status}"