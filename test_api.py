#!/usr/bin/env python3
"""
VARTAPRAVAH API Test Script
Test all endpoints with example requests
"""

import requests
import json
import time
from typing import Dict, Any

API_BASE = "http://localhost:8000"
STREAM_KEY = "qcu7-xesd-m4sv-9zvv-e335"
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

def print_response(response: requests.Response, title: str):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"🔹 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)

def test_health():
    """Test health check endpoint"""
    response = requests.get(f"{API_BASE}/health")
    print_response(response, "Health Check")
    return response.status_code == 200

def test_info():
    """Get API info"""
    response = requests.get(f"{API_BASE}/info")
    print_response(response, "API Information")
    return response.status_code == 200

def test_tts():
    """Test Text-to-Speech endpoint"""
    payload = {
        "text": "नमस्कार, वार्ताप्रवाह मध्ये आपले स्वागत आहे।",
        "output_path": "output/test_audio.wav"
    }
    
    response = requests.post(f"{API_BASE}/tts", json=payload)
    print_response(response, "Text-to-Speech Generation")
    
    if response.status_code == 200:
        data = response.json()
        return data.get("audio_path")
    return None

def test_lipsync(audio_path: str):
    """Test Lip-Sync endpoint"""
    if not audio_path:
        print("⚠️  Skipping lip-sync test - no audio path")
        return None
    
    payload = {
        "audio_path": audio_path,
        "video_path": "assets/anchor.mp4",
        "output_video": "output/test_video.mp4"
    }
    
    response = requests.post(f"{API_BASE}/lipsync", json=payload)
    print_response(response, "Lip-Sync Video Generation")
    
    if response.status_code == 200:
        data = response.json()
        return data.get("video_path")
    return None

def test_stream(video_path: str):
    """Test Streaming endpoint"""
    if not video_path:
        print("⚠️  Skipping stream test - no video path")
        return
    
    payload = {
        "video_path": video_path,
        "rtmp_url": RTMP_URL
    }
    
    response = requests.post(f"{API_BASE}/stream", json=payload)
    print_response(response, "YouTube Live Streaming (Background)")

def test_pipeline():
    """Test complete pipeline endpoint"""
    payload = {
        "text": "यह एक संपूर्ण पाइपलाइन परीक्षण है।",
        "rtmp_url": RTMP_URL
    }
    
    response = requests.post(f"{API_BASE}/pipeline", json=payload)
    print_response(response, "Complete Pipeline (TTS + Lip-Sync + Stream)")

def test_error_handling():
    """Test error handling with invalid requests"""
    
    # Test empty text
    payload = {"text": ""}
    response = requests.post(f"{API_BASE}/tts", json=payload)
    print_response(response, "Error Test - Empty Text")
    
    # Test missing audio file
    payload = {
        "audio_path": "nonexistent.wav",
        "video_path": "assets/anchor.mp4",
        "output_video": "output/test.mp4"
    }
    response = requests.post(f"{API_BASE}/lipsync", json=payload)
    print_response(response, "Error Test - Missing Audio File")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("VARTAPRAVAH API Test Suite")
    print("="*60)
    print(f"\nTesting API at: {API_BASE}")
    print(f"Stream Key: {STREAM_KEY[:10]}...")
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
    except requests.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API at", API_BASE)
        print("Make sure the container is running:")
        print("  docker-compose up -d")
        return
    
    # Run tests
    print("\n📋 Running Tests...\n")
    
    # 1. Health check
    if not test_health():
        print("❌ Health check failed!")
        return
    
    # 2. API info
    test_info()
    
    # 3. Text-to-Speech
    audio_path = test_tts()
    time.sleep(2)
    
    # 4. Lip-Sync (requires anchor.mp4 to exist)
    video_path = test_lipsync(audio_path)
    
    # 5. Streaming (background task)
    if video_path:
        test_stream(video_path)
    
    # 6. Complete Pipeline
    print("\n⏳ Testing complete pipeline (this may take time)...")
    test_pipeline()
    
    # 7. Error Handling
    print("\n🧪 Testing error handling...\n")
    test_error_handling()
    
    print("\n" + "="*60)
    print("✅ Test Suite Complete!")
    print("="*60)
    print("\n📖 API Documentation: http://localhost:8000/docs")
    print("📊 API Info: http://localhost:8000/info")
    print("💚 Health Check: http://localhost:8000/health")

if __name__ == "__main__":
    main()
