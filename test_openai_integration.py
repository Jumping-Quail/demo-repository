#!/usr/bin/env python3
"""
Test OpenAI Integration

This script tests the OpenAI integration by running a simple query
and verifying that the API key is properly configured.
"""

import os
import sys
import logging
from openai_config import get_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_openai_integration():
    """Test OpenAI integration"""
    print("🔍 Testing OpenAI Integration...")
    
    # Check if OpenAI API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set.")
        return False
    
    try:
        # Get OpenAI client
        client = get_client()
        
        # Test a simple query
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello!"}
            ],
            max_tokens=10
        )
        
        # Print response
        print(f"✅ OpenAI API test successful.")
        print(f"Response: {response.choices[0].message.content}")
        print(f"Model: {response.model}")
        
        # Test token counting
        text = "This is a test of the token counting functionality."
        token_count = client.count_tokens(text)
        print(f"Token count for '{text}': {token_count}")
        
        # Test chunking
        long_text = "This is a longer text that will be split into chunks. " * 10
        chunks = client.chunk_text(long_text, max_chunk_tokens=20)
        print(f"Split into {len(chunks)} chunks.")
        
        return True
    except Exception as e:
        print(f"❌ Error testing OpenAI integration: {str(e)}")
        logger.exception("Error testing OpenAI integration")
        return False

def main():
    """Main execution function"""
    success = test_openai_integration()
    
    if success:
        print("✅ OpenAI integration test passed!")
        return 0
    else:
        print("❌ OpenAI integration test failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
