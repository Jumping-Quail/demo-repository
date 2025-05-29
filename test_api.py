#!/usr/bin/env python3
"""
Test client for Mistral AI Repository Analysis API
Demonstrates all available endpoints and functionality
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:3001"

def test_endpoint(endpoint, method="GET", description=""):
    """Test a single API endpoint"""
    print(f"\n{'='*60}")
    print(f"Testing: {method} {endpoint}")
    print(f"Description: {description}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(f"{API_BASE_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{API_BASE_URL}{endpoint}")
        
        print(f"Status Code: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))
        else:
            print("Response:")
            print(response.text)
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run comprehensive API tests"""
    print("🚀 Mistral AI Repository Analysis API Test Suite")
    print("=" * 60)
    
    # Test all endpoints
    tests = [
        ("/", "GET", "API information and available endpoints"),
        ("/health", "GET", "Health check endpoint"),
        ("/test", "GET", "Quick test endpoint"),
        ("/analyze", "POST", "Run repository analysis"),
        ("/results", "GET", "Get analysis results"),
        ("/dashboard", "GET", "Dashboard information"),
    ]
    
    results = []
    
    for endpoint, method, description in tests:
        success = test_endpoint(endpoint, method, description)
        results.append((endpoint, method, success))
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, _, success in results if success)
    total = len(results)
    
    for endpoint, method, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {method:4} {endpoint}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API server.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)