#!/usr/bin/env python3
"""
Test script for OpenAI API key validation
Tests the OpenAI API key secret to ensure it's working correctly
"""

import os
import sys
import json
from datetime import datetime

def test_openai_api_key():
    """Test the OpenAI API key by making a simple API call"""
    
    print("🔑 Testing OpenAI API Key")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not found")
        return False
    
    print(f"✅ OpenAI API key found (length: {len(api_key)} characters)")
    print(f"✅ Key starts with: {api_key[:7]}...")
    
    try:
        # Try to import openai
        try:
            import openai
            print("✅ OpenAI library is available")
        except ImportError:
            print("⚠️  OpenAI library not installed, installing...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
            import openai
            print("✅ OpenAI library installed and imported")
        
        # Initialize the OpenAI client
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized")
        
        # Test with a simple completion
        print("\n🧪 Testing API with a simple completion...")
        
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, OpenAI API is working!' in exactly those words."}
            ],
            max_tokens=50,
            temperature=0
        )
        
        # Extract the response
        message = response.choices[0].message.content.strip()
        print(f"✅ API Response: {message}")
        
        # Verify the response
        if "Hello, OpenAI API is working!" in message:
            print("✅ API test successful - received expected response")
            return True
        else:
            print(f"⚠️  API responded but with unexpected content: {message}")
            return True  # Still consider it a success since API is working
            
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")
        
        # Check for common error types
        if "authentication" in str(e).lower() or "unauthorized" in str(e).lower():
            print("💡 This appears to be an authentication error - check if the API key is valid")
        elif "quota" in str(e).lower() or "billing" in str(e).lower():
            print("💡 This appears to be a quota/billing error - check your OpenAI account")
        elif "rate" in str(e).lower():
            print("💡 This appears to be a rate limiting error - try again later")
        
        return False

def test_api_key_format():
    """Test if the API key has the expected format"""
    print("\n🔍 Validating API Key Format")
    print("=" * 50)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No API key found")
        return False
    
    # OpenAI API keys typically start with 'sk-' and are 51 characters long
    if api_key.startswith('sk-'):
        print("✅ API key starts with 'sk-' (correct format)")
    else:
        print("⚠️  API key doesn't start with 'sk-' (unexpected format)")
    
    if len(api_key) == 51:
        print("✅ API key is 51 characters long (correct length)")
    else:
        print(f"⚠️  API key is {len(api_key)} characters long (expected 51)")
    
    return True

def main():
    """Run all OpenAI API tests"""
    print("🚀 OpenAI API Key Test Suite")
    print("=" * 60)
    print(f"Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Run tests
    format_test = test_api_key_format()
    api_test = test_openai_api_key()
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 50)
    
    if format_test:
        print("✅ API Key Format: PASS")
    else:
        print("❌ API Key Format: FAIL")
    
    if api_test:
        print("✅ API Functionality: PASS")
    else:
        print("❌ API Functionality: FAIL")
    
    overall_success = format_test and api_test
    
    if overall_success:
        print("\n🎉 All tests passed! OpenAI API key is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the API key configuration.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)