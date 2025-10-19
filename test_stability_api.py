#!/usr/bin/env python
"""
Quick test to check if Stability AI API key is valid
"""
import requests
from config import Config

def test_stability_api():
    print("=" * 60)
    print("TESTING STABILITY AI API CONNECTION")
    print("=" * 60)
    
    api_key = Config.STABILITY_API_KEY
    api_host = Config.STABILITY_API_HOST
    
    print(f"\n✓ API Key: {api_key[:20]}..." if api_key else "✗ No API Key")
    print(f"✓ API Host: {api_host}")
    
    # Test 1: Check if API key is set
    if not api_key or api_key == '':
        print("\n❌ ERROR: No API key found!")
        print("   Please set STABILITY_API_KEY in your .env file")
        return False
    
    # Test 2: Try to list available engines
    print("\n⏳ Testing API connection...")
    try:
        url = f"{api_host}/v1/engines/list"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS! API key is VALID and working!")
            engines = response.json()
            print(f"   Available engines: {len(engines)} found")
            return True
        elif response.status_code == 401:
            print("\n❌ AUTHENTICATION FAILED!")
            print("   Your API key is INVALID or EXPIRED")
            print(f"   Response: {response.text}")
            return False
        else:
            print(f"\n⚠️  API returned error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n❌ CONNECTION TIMEOUT")
        print("   Cannot reach Stability AI servers")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_stability_api()

