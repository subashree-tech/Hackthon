#!/usr/bin/env python
"""
Test script to verify the API is working correctly
Run this after starting the Flask app to test endpoints
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_health():
    """Test the health check endpoint"""
    print("\n" + "="*50)
    print("Testing Health Check Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"   Status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is the Flask app running?")
        print("   Start it with: python run.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_generate():
    """Test the image generation endpoint"""
    print("\n" + "="*50)
    print("Testing Image Generation Endpoint")
    print("="*50)
    
    test_prompt = "A simple cartoon cat"
    print(f"Prompt: '{test_prompt}'")
    print("Generating image (this may take 10-30 seconds)...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json={"prompt": test_prompt},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Image generation successful!")
            print(f"   Image URL: {data.get('image_url')}")
            print(f"   Timestamp: {data.get('timestamp')}")
            return True
        else:
            print(f"❌ Image generation failed with status {response.status_code}")
            error_data = response.json()
            print(f"   Error: {error_data.get('error', 'Unknown error')}")
            return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out. This might mean:")
        print("   - Stability AI API is slow")
        print("   - Network issues")
        print("   - Invalid API key")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_invalid_request():
    """Test error handling with invalid request"""
    print("\n" + "="*50)
    print("Testing Error Handling")
    print("="*50)
    
    try:
        # Test with empty prompt
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json={"prompt": ""},
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Error handling works correctly!")
            print("   Server properly rejects empty prompts")
            return True
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("API Test Suite for Kids Coloring Page Generator")
    print("="*60)
    
    print("\nMake sure the Flask app is running before running these tests!")
    print("Start it with: python run.py")
    
    input("\nPress Enter to start tests...")
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("Error Handling", test_invalid_request()))
    results.append(("Image Generation", test_generate()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print("\n" + "="*60)
    print(f"Results: {passed_count}/{total_count} tests passed")
    print("="*60)
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! Your app is working correctly!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("Common issues:")
        print("  - Missing or invalid API keys in .env file")
        print("  - Flask app not running")
        print("  - Dependencies not installed")
    
    return 0 if passed_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())

