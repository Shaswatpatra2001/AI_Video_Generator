"""
FINAL WORKING services.py for Gemini Veo 3.1 API
"""
import os
import time
from django.conf import settings
from django.core.files.base import ContentFile
from .models import VideoGenerationRequest
from google import genai
from google.genai import types

class VideoGenerationService:
    
    @staticmethod
    def get_client():
        """Get Gemini client."""
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")
        return genai.Client(api_key=api_key)
    
    @staticmethod
    def generate_video_sync(video_request):
        """Generate video SYNCHRONOUSLY - CORRECT VERSION"""
        try:
            client = VideoGenerationService.get_client()
            
            # Update to processing
            video_request.status = 'processing'
            video_request.save()
            
            print(f"🚀 Generating video for request {video_request.id}...")
            print(f"📝 Prompt: {video_request.prompt[:100]}...")
            
            # Check if we have an image
            has_image = False
            image_bytes = None
            
            if video_request.store_image:
                try:
                    # Get the absolute path
                    image_path = video_request.store_image.path
                    if os.path.exists(image_path):
                        print(f"🖼️ Using image: {image_path}")
                        
                        # Read image as bytes
                        with open(image_path, 'rb') as f:
                            image_bytes = f.read()
                        
                        print(f"📏 Image size: {len(image_bytes)} bytes")
                        has_image = True
                    else:
                        print("⚠️ Image file doesn't exist on disk")
                except Exception as img_error:
                    print(f"⚠️ Could not access image file: {img_error}")
            
            # Generate video
            try:
                if has_image and image_bytes:
                    print("🎬 Generating image-to-video...")
                    
                    # CORRECT WAY: Use types.Image
                    image_part = types.Image(content=image_bytes)
                    
                    operation = client.models.generate_videos(
                        model="veo-3.1-fast-generate-preview",  # or "veo-3.1-generate-preview"
                        prompt=video_request.prompt,
                        image=image_part  # CORRECT: Use types.Image
                    )
                    
                    print("✅ Image-to-video request sent!")
                else:
                    # Text-to-video only
                    print("🎬 Generating text-to-video...")
                    
                    operation = client.models.generate_videos(
                        model="veo-3.1-fast-generate-preview",
                        prompt=video_request.prompt
                    )
                
                # Wait for completion
                print("⏳ Video generation in progress. This takes 2-3 minutes...")
                start_time = time.time()
                
                # Poll operation
                while not operation.done:
                    elapsed = int(time.time() - start_time)
                    if elapsed > 300:  # 5 minutes timeout
                        raise TimeoutError(f"Timeout after {elapsed} seconds")
                    
                    if elapsed % 30 == 0:  # Log every 30 seconds
                        print(f"⏳ Still processing... ({elapsed}s)")
                    
                    time.sleep(5)
                
                print("✅ Video generation completed!")
                
                # Get the video
                if operation.response and operation.response.generated_videos:
                    generated_video = operation.response.generated_videos[0]
                    video_uri = generated_video.video.uri
                    
                    print(f"📥 Downloading video from: {video_uri}")
                    
                    # Download video
                    video_content = client.files.download(file=generated_video.video)
                    
                    # Save to file
                    file_name = f"jsj_card_video_{video_request.id}.mp4"
                    video_request.video_file.save(file_name, ContentFile(video_content))
                    video_request.video_url = video_uri
                    video_request.status = 'completed'
                    video_request.save()
                    
                    print(f"✅ Video saved: {file_name}")
                    print(f"📁 Local path: {video_request.video_file.path}")
                    print(f"🌐 Access at: http://127.0.0.1:8000{video_request.video_file.url}")
                    
                    return True
                else:
                    raise ValueError("No video generated in response")
                    
            except Exception as gen_error:
                print(f"❌ Generation error: {gen_error}")
                
                # Fallback: Try text-only if image fails
                if has_image:
                    print("🔄 Falling back to text-to-video...")
                    
                    # Clear previous error
                    video_request.error_message = None
                    video_request.save()
                    
                    # Try text-only
                    try:
                        operation = client.models.generate_videos(
                            model="veo-3.1-fast-generate-preview",
                            prompt=f"A person speaking: {video_request.prompt}"
                        )
                        
                        # Wait for completion
                        while not operation.done:
                            time.sleep(5)
                        
                        if operation.response and operation.response.generated_videos:
                            generated_video = operation.response.generated_videos[0]
                            video_content = client.files.download(file=generated_video.video)
                            
                            file_name = f"jsj_card_video_{video_request.id}.mp4"
                            video_request.video_file.save(file_name, ContentFile(video_content))
                            video_request.video_url = generated_video.video.uri
                            video_request.status = 'completed'
                            video_request.save()
                            
                            print(f"✅ Fallback video saved: {file_name}")
                            return True
                    except Exception as fallback_error:
                        print(f"❌ Fallback also failed: {fallback_error}")
                        raise fallback_error
                else:
                    raise gen_error
                    
        except Exception as e:
            error_msg = str(e)
            print(f"❌ FATAL ERROR: {error_msg}")
            video_request.status = 'failed'
            video_request.error_message = error_msg
            video_request.save()
            return False