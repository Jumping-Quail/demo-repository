#!/usr/bin/env python3
"""
Comprehensive OpenAI API test suite
Tests various OpenAI API endpoints and capabilities
"""

import os
import sys
import json
import time
from datetime import datetime

def test_chat_completion():
    """Test chat completion endpoint"""
    print("\n💬 Testing Chat Completion")
    print("-" * 40)
    
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": "Write a simple Python function that adds two numbers."}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        message = response.choices[0].message.content
        print(f"✅ Chat completion successful")
        print(f"Response preview: {message[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Chat completion failed: {str(e)}")
        return False

def test_text_completion():
    """Test text completion endpoint (legacy)"""
    print("\n📝 Testing Text Completion")
    print("-" * 40)
    
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Note: text completion models are being deprecated, but we can test with gpt-3.5-turbo-instruct
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt="The benefits of using Python for data science include:",
            max_tokens=100,
            temperature=0.5
        )
        
        text = response.choices[0].text.strip()
        print(f"✅ Text completion successful")
        print(f"Response preview: {text[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Text completion failed: {str(e)}")
        return False

def test_embeddings():
    """Test embeddings endpoint"""
    print("\n🔢 Testing Embeddings")
    print("-" * 40)
    
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input="This is a test sentence for embedding generation."
        )
        
        embedding = response.data[0].embedding
        print(f"✅ Embeddings successful")
        print(f"Embedding dimensions: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Embeddings failed: {str(e)}")
        return False

def test_models_list():
    """Test listing available models"""
    print("\n📋 Testing Models List")
    print("-" * 40)
    
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        models = client.models.list()
        model_names = [model.id for model in models.data]
        
        print(f"✅ Models list successful")
        print(f"Total models available: {len(model_names)}")
        
        # Show some popular models if available
        popular_models = ['gpt-4', 'gpt-3.5-turbo', 'text-embedding-ada-002', 'whisper-1']
        available_popular = [model for model in popular_models if model in model_names]
        
        if available_popular:
            print(f"Popular models available: {', '.join(available_popular)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Models list failed: {str(e)}")
        return False

def test_usage_tracking():
    """Test API usage tracking"""
    print("\n📊 Testing Usage Tracking")
    print("-" * 40)
    
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Make a small request and track tokens
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Count to 5."}
            ],
            max_tokens=50
        )
        
        usage = response.usage
        print(f"✅ Usage tracking successful")
        print(f"Prompt tokens: {usage.prompt_tokens}")
        print(f"Completion tokens: {usage.completion_tokens}")
        print(f"Total tokens: {usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ Usage tracking failed: {str(e)}")
        return False

def test_streaming():
    """Test streaming responses"""
    print("\n🌊 Testing Streaming")
    print("-" * 40)
    
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        print("Streaming response: ", end="", flush=True)
        
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Streaming test successful!' word by word."}
            ],
            max_tokens=50,
            stream=True
        )
        
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        
        print()  # New line
        print(f"✅ Streaming successful")
        print(f"Full response: {full_response.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Streaming failed: {str(e)}")
        return False

def main():
    """Run comprehensive OpenAI API tests"""
    print("🚀 Comprehensive OpenAI API Test Suite")
    print("=" * 60)
    print(f"Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not found")
        return False
    
    print(f"🔑 Using API key: {api_key[:10]}...{api_key[-4:]}")
    
    # Run tests
    tests = [
        ("Chat Completion", test_chat_completion),
        ("Text Completion", test_text_completion),
        ("Embeddings", test_embeddings),
        ("Models List", test_models_list),
        ("Usage Tracking", test_usage_tracking),
        ("Streaming", test_streaming),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
            time.sleep(1)  # Brief pause between tests to avoid rate limiting
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 COMPREHENSIVE TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! OpenAI API is fully functional.")
    elif passed > 0:
        print("⚠️  Some tests passed. API is partially functional.")
    else:
        print("❌ All tests failed. Check API key and connectivity.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)