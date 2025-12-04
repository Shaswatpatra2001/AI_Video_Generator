"""
DEBUG FILE - FIXED VERSION
"""
import os
import sys
import time
from django.conf import settings

# Add Django setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_video_generator.settings')

import django
django.setup()

from google import genai
from videos.models import VideoGenerationRequest

def debug_gemini_api():
    """Debug Gemini API to see exact error"""
    
    print("=" * 60)
    print("DEBUGGING GEMINI VEO API - FIXED")
    print("=" * 60)
    
    # 1. Check API Key
    api_key = settings.GEMINI_API_KEY
    print(f"1. API Key check: {'✓ Set' if api_key else '✗ Missing'}")
    
    # 2. Initialize client
    try:
        client = genai.Client(api_key=api_key)
        print("2. Client initialized: ✓")
    except Exception as e:
        print(f"2. Client init error: {e}")
        return
    
    # 3. Test without image (text-to-video)
    print("\n3. Testing TEXT-TO-VIDEO...")
    try:
        result = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt="A person smiling and speaking to camera"
        )
        print(f"   Operation name: {result.name}")
        print("   Text-to-video: ✓ SUCCESS")
    except Exception as e:
        print(f"   Text-to-video error: {e}")
    
    # 4. Create a test image and test
    print("\n4. Creating test image and testing...")
    
    # Create a simple test image file
    test_image_path = "test_image.jpg"
    
    # Create a simple colored image using PIL
    try:
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (500, 500), color='blue')
        draw = ImageDraw.Draw(img)
        draw.text((50, 250), "TEST IMAGE", fill='white')
        img.save(test_image_path)
        print(f"   Created test image: {test_image_path}")
    except:
        # If PIL not available, create a dummy file
        with open(test_image_path, 'wb') as f:
            f.write(b'dummy')
        print(f"   Created dummy test file")
    
    # Read test image
    with open(test_image_path, 'rb') as f:
        test_image_bytes = f.read()
    
    print(f"   Test image size: {len(test_image_bytes)} bytes")
    
    # Test DIRECT approach (what should work)
    print("\n   Testing CORRECT format...")
    try:
        # The CORRECT way based on Gemini documentation
        result = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt="A person speaking",
            image=test_image_bytes  # Just raw bytes
        )
        print(f"   ✓ SUCCESS with raw bytes!")
        print(f"   Operation: {result.name}")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
        print(f"   Error type: {type(e)}")
        
        # Try different approach
        print("\n   Trying alternative approach...")
        try:
            # Try as File object
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                tmp.write(test_image_bytes)
                tmp_path = tmp.name
            
            result = client.models.generate_videos(
                model="veo-3.1-fast-generate-preview",
                prompt="A person speaking",
                image=tmp_path  # File path
            )
            print(f"   ✓ SUCCESS with file path!")
            os.unlink(tmp_path)  # Cleanup
        except Exception as e2:
            print(f"   ✗ Also failed: {e2}")
    
    # 5. Show API documentation info
    print("\n5. API Documentation Info:")
    print("   Model: veo-3.1-fast-generate-preview")
    print("   Image should be: bytes or file path")
    
    # Cleanup
    if os.path.exists(test_image_path):
        os.remove(test_image_path)
    
    print("\n" + "=" * 60)
    print("DEBUG COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    print("Starting Gemini Veo Debug...")
    debug_gemini_api()