import requests
import time

API_KEY = "sk_V2_hgu_k4sG4Sz2pyd_07KhpzALRR2Qk2q1vecc1wPqpBrDjNhc"
headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

print("=" * 60)
print("FINDING WORKING HEYGEN AVATARS")
print("=" * 60)

print("\n1. Trying to find correct avatar endpoint...")
print("-" * 40)

# Try different avatar listing endpoints
endpoints = [
    "https://api.heygen.com/v2/avatars",
    "https://api.heygen.com/v1/avatars",
    "https://api.heygen.com/avatars",
    "https://api.heygen.com/v1/avatar.list",
    "https://api.heygen.com/v1/avatar"
]

for endpoint in endpoints:
    try:
        print(f"\nTrying: {endpoint}")
        resp = requests.get(endpoint, headers=headers, timeout=10)
        print(f"   Status: {resp.status_code}")
        
        if resp.status_code == 200:
            print(f"   ✅ SUCCESS!")
            data = resp.json()
            print(f"   Response: {data}")
            break
        elif resp.status_code in [400, 404]:
            print(f"   Response: {resp.text[:200]}")
        else:
            print(f"   Response: {resp.text[:100]}")
            
        time.sleep(1)  # Avoid rate limiting
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")

print("\n" + "=" * 60)
print("2. Testing KNOWN WORKING AVATARS from HeyGen Docs")
print("=" * 60)

# From HeyGen documentation, these should work:
known_avatars = [
    # Basic avatars
    {"id": "1", "name": "Basic Male"},
    {"id": "2", "name": "Basic Female"},
    
    # Common avatars from docs
    {"id": "Danny_costume1_cameraA", "name": "Danny"},
    {"id": "Samantha_costume1_cameraA", "name": "Samantha"},
    {"id": "Anna_costume1_cameraA", "name": "Anna"},
    {"id": "Will_costume1_cameraA", "name": "Will"},
    
    # Other possible formats
    {"id": "danny", "name": "danny lowercase"},
    {"id": "samantha", "name": "samantha lowercase"},
    {"id": "anna", "name": "anna lowercase"},
    
    # Numeric IDs
    {"id": "101", "name": "101"},
    {"id": "102", "name": "102"},
    {"id": "201", "name": "201"},
    {"id": "202", "name": "202"},
]

print("\nTesting each avatar with SIMPLE payload...")
print("-" * 40)

# Simple minimal payload
simple_payload = {
    "video_inputs": [{
        "character": {
            "type": "avatar", 
            "avatar_id": "",
            "avatar_style": "normal"
        },
        "voice": {
            "type": "text",
            "input_text": "Test",
            "voice_id": "1bd001e7e50f421d891986aad5158bc8"
        },
        "background": {"type": "color", "value": "#FFFFFF"}
    }],
    "dimension": {"width": 1280, "height": 720},
    "test": True
}

working_avatars = []

for avatar in known_avatars:
    print(f"\nTesting: {avatar['name']} (ID: {avatar['id']})")
    
    # Update avatar_id
    test_payload = simple_payload.copy()
    test_payload["video_inputs"][0]["character"]["avatar_id"] = avatar['id']
    
    try:
        resp = requests.post("https://api.heygen.com/v2/video/generate", 
                            json=test_payload, headers=headers, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✅ Status 200 - Code: {data.get('code')}")
            
            if data.get('code') == 100:
                print(f"   🎉 SUCCESS! Avatar works!")
                working_avatars.append(avatar)
                print(f"   Video ID: {data.get('data', {}).get('video_id')}")
            else:
                print(f"   ❌ API Error: {data.get('message', 'Unknown')}")
        elif resp.status_code == 404:
            data = resp.json()
            print(f"   ❌ 404 - {data.get('error', {}).get('message', 'Unknown')}")
        elif resp.status_code == 429:
            print(f"   ⚠️  Rate limited (429). Waiting 10 seconds...")
            time.sleep(10)
            continue
        else:
            print(f"   ❌ HTTP {resp.status_code}: {resp.text[:100]}")
            
        # Wait to avoid rate limiting
        time.sleep(2)
        
    except Exception as e:
        print(f"   ❌ Exception: {str(e)[:50]}")
        time.sleep(2)

print("\n" + "=" * 60)
print("3. TESTING SIMPLEST POSSIBLE PAYLOAD")
print("=" * 60)

print("\nTrying absolute minimum payload...")
minimal_payload = {
    "video_inputs": [{
        "character": {"type": "avatar", "avatar_id": "1"},
        "voice": {"type": "text", "input_text": "Test", "voice_id": "1"}
    }],
    "test": True
}

try:
    resp = requests.post("https://api.heygen.com/v2/video/generate", 
                        json=minimal_payload, headers=headers, timeout=15)
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.text}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
print("RESULTS SUMMARY")
print("=" * 60)

if working_avatars:
    print(f"\n✅ FOUND {len(working_avatars)} WORKING AVATARS:")
    for avatar in working_avatars:
        print(f"   - {avatar['name']} (ID: {avatar['id']})")
else:
    print("\n❌ NO WORKING AVATARS FOUND")
    print("\nPossible issues:")
    print("1. API key doesn't have avatar access")
    print("2. Need to enable avatars in HeyGen dashboard")
    print("3. Account needs upgrade for avatar access")
    print("4. Contact HeyGen support")

print("\n" + "=" * 60)
print("NEXT STEPS")
print("=" * 60)

print("""
1. Check HeyGen dashboard: https://app.heygen.com
2. Go to Avatar Studio to see available avatars
3. Contact support if no avatars work
4. Try creating a video manually in HeyGen app first
5. Check billing/credits status
""")