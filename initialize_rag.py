#!/usr/bin/env python3
"""
Initialize RAG System

This script initializes the RAG system by processing repository documentation
and analysis reports, generating embeddings, and creating the vector store.
"""

import os
import sys
import logging
from rag_system import initialize_rag_system

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main execution function"""
    print("🔍 Initializing RAG System...")
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️ Warning: OPENAI_API_KEY environment variable not set.")
        print("   The RAG system will use random embeddings for testing purposes.")
        print("   For production use, please set the OPENAI_API_KEY environment variable.")
    
    # Force reinitialization if specified
    force = '--force' in sys.argv
    
    # Initialize the RAG system
    success = initialize_rag_system(force=force)
    
    if success:
        print("✅ RAG System initialized successfully!")
        print("   You can now query the system using the /rag-query endpoint.")
    else:
        print("❌ Failed to initialize RAG System.")
        print("   Please check the logs for more information.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
