import requests

API_KEY = "sk_V2_hgu_k4sG4Sz2pyd_07KhpzALRR2Qk2q1vecc1wPqpBrDjNhc"
headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

print("=" * 60)
print("HEYGEN API ENDPOINT TESTER")
print("=" * 60)

print("\n1. First, let's check if API key is valid...")
print("-" * 40)

# Try to list available avatars (different endpoints)
avatar_endpoints = [
    "https://api.heygen.com/v1/avatars.list",
    "https://api.heygen.com/v1/avatars",
    "https://api.heygen.com/v2/avatars"
]

for endpoint in avatar_endpoints:
    try:
        print(f"\nTrying: {endpoint}")
        resp = requests.get(endpoint, headers=headers, timeout=10)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"   ✅ SUCCESS! Response: {resp.text[:200]}")
            break
        else:
            print(f"   ❌ Failed: {resp.text[:100]}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")

print("\n" + "=" * 60)
print("2. Testing VIDEO GENERATION Endpoints")
print("=" * 60)

# Test 1: v2 endpoint with correct payload
print("\n🎬 TEST 1: v2/video/generate (with correct payload)")
print("-" * 40)

payload_v2 = {
    "video_inputs": [{
        "character": {
            "type": "avatar", 
            "avatar_id": "Danny",
            "avatar_style": "normal"
        },
        "voice": {
            "type": "text",
            "input_text": "Testing HeyGen v2 API for merchant video generation",
            "voice_id": "1bd001e7e50f421d891986aad5158bc8"
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
    "test": True,  # Test mode (won't use credits)
    "caption": False
}

try:
    resp = requests.post("https://api.heygen.com/v2/video/generate", 
                        json=payload_v2, headers=headers, timeout=30)
    print(f"   Endpoint: https://api.heygen.com/v2/video/generate")
    print(f"   Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"   ✅ SUCCESS! Response code: {data.get('code')}")
        print(f"   Message: {data.get('message')}")
        
        if data.get('code') == 100:  # HeyGen success code
            if data.get('data'):
                print(f"   🎉 VIDEO CREATED!")
                print(f"   Video ID: {data['data'].get('video_id')}")
                print(f"   Video URL: {data['data'].get('video_url')}")
                
                if data['data'].get('video_id'):
                    print(f"   Share URL: https://app.heygen.com/share/{data['data']['video_id']}")
        else:
            print(f"   ❌ API Error: {data.get('message')}")
            print(f"   Full response: {data}")
    
    else:
        print(f"   ❌ HTTP Error: {resp.status_code}")
        print(f"   Response: {resp.text[:200]}")
        
except Exception as e:
    print(f"   ❌ Exception: {str(e)}")

print("\n" + "=" * 60)
print("3. Testing with TEST=False (Real Video)")
print("=" * 60)

# Test 2: Try with test=False (real video using credits)
print("\n🎬 TEST 2: v2/video/generate (test=False - REAL VIDEO)")
print("-" * 40)

payload_real = payload_v2.copy()
payload_real["test"] = False  # Real video (uses 1 credit)

print("⚠️  WARNING: This will use 1 credit from your 10 Free tier credits!")
user_input = input("Continue? (y/n): ")

if user_input.lower() == 'y':
    try:
        resp = requests.post("https://api.heygen.com/v2/video/generate", 
                            json=payload_real, headers=headers, timeout=60)
        print(f"\n   Endpoint: https://api.heygen.com/v2/video/generate")
        print(f"   Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Response code: {data.get('code')}")
            
            if data.get('code') == 100:
                print(f"   🎉 REAL VIDEO CREATED! (Used 1 credit)")
                print(f"   Video ID: {data['data'].get('video_id')}")
                print(f"   Video URL: {data['data'].get('video_url')}")
                
                if data['data'].get('video_id'):
                    # Try to get video status
                    print(f"\n   🔍 Getting video status...")
                    status_resp = requests.get(
                        f"https://api.heygen.com/v1/video_status.get?video_id={data['data']['video_id']}",
                        headers=headers
                    )
                    if status_resp.status_code == 200:
                        status_data = status_resp.json()
                        print(f"   Status: {status_data.get('data', {}).get('status')}")
            else:
                print(f"   ❌ Error: {data.get('message')}")
        else:
            print(f"   ❌ HTTP Error: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
else:
    print("   Skipped real video test.")

print("\n" + "=" * 60)
print("4. Testing Different Avatars")
print("=" * 60)

# Test different avatars
avatars_to_test = ["Danny", "Samantha", "1", "Anna", "Will"]

for avatar in avatars_to_test:
    print(f"\nTesting avatar: {avatar}")
    test_payload = payload_v2.copy()
    test_payload["video_inputs"][0]["character"]["avatar_id"] = avatar
    
    try:
        resp = requests.post("https://api.heygen.com/v2/video/generate", 
                            json=test_payload, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('code') == 100:
                print(f"   ✅ {avatar} - Works!")
            else:
                print(f"   ❌ {avatar} - Error: {data.get('message', 'Unknown')}")
        else:
            print(f"   ❌ {avatar} - HTTP {resp.status_code}")
            
    except Exception as e:
        print(f"   ❌ {avatar} - Exception: {str(e)[:50]}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
Based on your previous test results:
1. ✅ v2/video/generate endpoint EXISTS (returns 400, not 404)
2. ❌ All v1 endpoints return 404 (not found)
3. The error was: "voice_id is invalid: Field required"

SOLUTION:
- Use ONLY: https://api.heygen.com/v2/video/generate
- Include 'voice_id' in voice object
- Format payload correctly for v2 API
- Use test=True for testing, test=False for real videos
""")

print("\nNext steps:")
print("1. Run this script to see if v2 works with correct payload")
print("2. If success, update your Django services.py")
print("3. Create real videos with test=False")