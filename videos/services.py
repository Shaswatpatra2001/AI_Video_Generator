import requests
import base64
from django.utils import timezone
from .models import VideoGenerationRequest
import os

class VideoGenerationService:
    
    HEYGEN_API_KEY = "sk_V2_hgu_k4sG4Sz2pyd_07KhpzALRR2Qk2q1vecc1wPqpBrDjNhc"
    
    @staticmethod
    def create_video_generation_request(store_image, product_image, offer_text, location):
        try:
            video_request = VideoGenerationRequest.objects.create(
                store_image=store_image,
                product_image=product_image,
                offer_text=offer_text,
                location=location
            )
            return video_request, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_video_request_by_id(request_id):
        try:
            video_request = VideoGenerationRequest.objects.get(id=request_id)
            return video_request, None
        except VideoGenerationRequest.DoesNotExist:
            return None, "Video request not found"
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_all_video_requests():
        try:
            video_requests = VideoGenerationRequest.objects.all().order_by('-created_at')
            return video_requests, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def update_video_request_status(request_id, status, video_url=None, error_message=None):
        try:
            video_request = VideoGenerationRequest.objects.get(id=request_id)
            video_request.status = status
            if video_url:
                video_request.generated_video_url = video_url
            if error_message:
                video_request.error_message = error_message
            video_request.updated_at = timezone.now()
            video_request.save()
            return video_request, None
        except VideoGenerationRequest.DoesNotExist:
            return None, "Video request not found"
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def generate_ai_video(video_request):
        try:
            headers = {
                "X-Api-Key": VideoGenerationService.HEYGEN_API_KEY,
                "Content-Type": "application/json"
            }
            
            # Create script from merchant data
            script = f"""
            Welcome to our store at {video_request.location}!
            
            {video_request.offer_text}
            
            Visit us today for great deals!
            """
            
            # Use a female avatar with matching female voice
            payload = {
                "video_inputs": [{
                    "character": {
                        "type": "avatar",
                        "avatar_id": "Samantha",  # Female avatar
                        "avatar_style": "normal"
                    },
                    "voice": {
                        "type": "text",
                        "input_text": script,
                        "voice_id": "1bd001e7e50f421d891986aad5158bc8"  # Female voice
                    },
                    "background": {
                        "type": "color",
                        "value": "#FFFFFF"
                    }
                }],
                "dimension": {
                    "width": 1280,
                    "height": 720
                },
                "test": True,  # Use TEST mode first to avoid credit usage
                "caption": False,
                "title": f"Store Promotion - {video_request.location}"
            }
            
            print(f"Creating AI video with script: {script[:100]}...")
            
            response = requests.post(
                "https://api.heygen.com/v1/video.generate",  # Use v1 endpoint
                json=payload,
                headers=headers,
                timeout=60
            )
            
            print(f"Response Status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Full Response: {data}")
                
                # Check for success
                if data.get('code') == 0:  # HeyGen success code
                    if data.get('data') and data['data'].get('video_url'):
                        video_url = data['data']['video_url']
                        print(f"✅ SUCCESS! Video URL: {video_url}")
                        return video_url, None
                    elif data.get('data') and data['data'].get('video_id'):
                        video_id = data['data']['video_id']
                        video_url = f"https://app.heygen.com/share/{video_id}"
                        print(f"✅ SUCCESS! Share URL: {video_url}")
                        return video_url, None
                
                # If API returned error
                error_msg = data.get('msg', str(data))
                return None, f"HeyGen API Error: {error_msg}"
            
            # If HTTP error
            return None, f"HTTP {response.status_code}: {response.text[:100]}"
                
        except Exception as e:
            print(f"Exception: {str(e)}")
            return None, str(e)