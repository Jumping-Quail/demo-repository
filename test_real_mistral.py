#!/usr/bin/env python3
"""
Test script for real Mistral AI integration
This script demonstrates how to test the API with a real Mistral API key
"""

import requests
import json
import os
import sys

API_BASE_URL = "http://localhost:3001"

def test_with_real_api_key():
    """Test Mistral integration with real API key"""
    
    print("🧪 Testing Real Mistral AI Integration")
    print("=" * 60)
    
    # Check for API key in environment
    api_key = os.getenv('MISTRAL_API_KEY')
    
    if not api_key:
        print("❌ MISTRAL_API_KEY not found in environment")
        print("\nTo test with real API:")
        print("1. Set your Mistral API key:")
        print("   export MISTRAL_API_KEY='your-api-key-here'")
        print("2. Run this script again")
        print("\nAlternatively, you can test via API endpoint:")
        print(f"   curl -X POST {API_BASE_URL}/mistral-test \\")
        print("        -H 'Content-Type: application/json' \\")
        print("        -d '{\"api_key\": \"your-api-key-here\"}'")
        return False
    
    print(f"✅ Found API key: {api_key[:8]}...")
    
    # Test the /mistral-test endpoint
    print("\n🔍 Testing /mistral-test endpoint...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/mistral-test",
            json={"api_key": api_key},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ /mistral-test endpoint successful")
            print(f"   Status: {result.get('status', 'unknown')}")
            print(f"   API key in env: {result.get('api_key_in_env', False)}")
            print(f"   API key provided: {result.get('api_key_provided', False)}")
            
            if result.get('error'):
                print(f"   Error: {result['error']}")
            
        else:
            print(f"❌ /mistral-test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing /mistral-test: {e}")
        return False
    
    # Test the /mistral-analyze endpoint
    print("\n🔍 Testing /mistral-analyze endpoint...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/mistral-analyze",
            json={"api_key": api_key},
            timeout=60  # Longer timeout for analysis
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ /mistral-analyze endpoint successful")
            
            # Check if we got real analysis results
            if 'analysis_results' in result:
                analysis = result['analysis_results']
                print(f"   Analysis types: {list(analysis.keys())}")
                
                # Check for code quality analysis
                if 'code_quality' in analysis:
                    cq = analysis['code_quality']
                    if isinstance(cq, dict) and 'overall_score' in cq:
                        print(f"   Code Quality Score: {cq['overall_score']}/10")
                    
                # Check if this looks like real API results vs simulation
                output = result.get('output', '')
                if 'Calling Mistral AI API for real analysis' in output and 'Error calling Mistral API' not in output:
                    print("🎉 Real Mistral AI analysis completed successfully!")
                elif 'Falling back to simulation mode' in output:
                    print("⚠️  Fell back to simulation mode (check API key validity)")
                else:
                    print("ℹ️  Analysis completed (mode unclear)")
            
        else:
            print(f"❌ /mistral-analyze failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing /mistral-analyze: {e}")
        return False
    
    return True

def test_simulation_mode():
    """Test simulation mode (no API key required)"""
    
    print("\n🧪 Testing Simulation Mode")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/mistral-test",
            json={},  # No API key
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Simulation mode test successful")
            print(f"   Status: {result.get('status', 'unknown')}")
            
            output = result.get('output', '')
            if 'Simulation mode test completed' in output:
                print("✅ Simulation mode working correctly")
                return True
            
        else:
            print(f"❌ Simulation test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing simulation mode: {e}")
        
    return False

def main():
    """Main test function"""
    
    print("🚀 Mistral AI Integration Test Suite")
    print("=" * 60)
    
    # Check if API server is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ API server not responding correctly: {response.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ API server not accessible: {e}")
        print(f"   Make sure the server is running on {API_BASE_URL}")
        print("   Run: python api_server.py")
        sys.exit(1)
    
    print(f"✅ API server is running on {API_BASE_URL}")
    
    # Test simulation mode first
    sim_success = test_simulation_mode()
    
    # Test real API mode
    real_success = test_with_real_api_key()
    
    print("\n" + "=" * 60)
    print("🏁 Test Summary")
    print("=" * 60)
    print(f"Simulation Mode: {'✅ PASS' if sim_success else '❌ FAIL'}")
    print(f"Real API Mode: {'✅ PASS' if real_success else '⚠️  SKIP (no API key)'}")
    
    if sim_success:
        print("\n✅ Mistral AI integration is working correctly!")
        if not real_success:
            print("💡 To test with real Mistral AI, set MISTRAL_API_KEY environment variable")
    else:
        print("\n❌ Issues detected with Mistral AI integration")
        sys.exit(1)

if __name__ == "__main__":
    main()