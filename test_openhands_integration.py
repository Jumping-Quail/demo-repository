#!/usr/bin/env python3
"""
Test OpenHands Integration

This script tests the OpenHands integration by running a simple query
and verifying that the API key is properly configured.
"""

import os
import sys
import logging
from openhands_config import get_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_openhands_integration():
    """Test OpenHands integration"""
    print("🔍 Testing OpenHands Integration...")
    
    # Check if OpenHands API key is set
    api_key = os.getenv('OPENHANDS_API_KEY')
    if not api_key:
        print("❌ OPENHANDS_API_KEY environment variable not set.")
        return False
    
    try:
        # Get OpenHands client
        client = get_client()
        
        # Test a simple query
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello!"}
            ],
            max_tokens=10,
            thinking="high"
        )
        
        # Print response
        print(f"✅ OpenHands API test successful.")
        print(f"Response: {response['choices'][0]['message']['content']}")
        print(f"Model: {response['model']}")
        
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
        print(f"❌ Error testing OpenHands integration: {str(e)}")
        logger.exception("Error testing OpenHands integration")
        return False

def main():
    """Main execution function"""
    success = test_openhands_integration()
    
    if success:
        print("✅ OpenHands integration test passed!")
        return 0
    else:
        print("❌ OpenHands integration test failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
