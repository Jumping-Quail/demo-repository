"""
OpenAI Configuration Module

This module handles the configuration and initialization of the OpenAI client,
including error handling, retry logic, and token management.
"""

import os
import time
import logging
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv
import openai
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "4096"))
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))

# Token limits for different models
MODEL_TOKEN_LIMITS = {
    "gpt-3.5-turbo": 16385,
    "gpt-4": 8192,
    "gpt-4-turbo": 128000,
    "gpt-4o": 128000,
}

class OpenAIClient:
    """
    A wrapper class for the OpenAI client with error handling and retry logic.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the OpenAI client.
        
        Args:
            api_key: OpenAI API key. If None, uses the environment variable.
            model: Default model to use. If None, uses the environment variable.
        """
        self.api_key = api_key or OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it explicitly.")
        
        self.model = model or DEFAULT_MODEL
        self.client = OpenAI(api_key=self.api_key)
        logger.info(f"OpenAI client initialized with model: {self.model}")
    
    @retry(
        retry=retry_if_exception_type((
            openai.RateLimitError,
            openai.APITimeoutError,
            openai.APIConnectionError
        )),
        wait=wait_exponential(multiplier=1, min=2, max=60),
        stop=stop_after_attempt(5)
    )
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to the OpenAI API with retry logic.
        
        Args:
            messages: List of message dictionaries.
            model: Model to use. If None, uses the default model.
            temperature: Temperature for sampling. If None, uses the default temperature.
            max_tokens: Maximum tokens to generate. If None, uses the default max tokens.
            **kwargs: Additional arguments to pass to the API.
            
        Returns:
            The API response.
        """
        model = model or self.model
        temperature = temperature or TEMPERATURE
        max_tokens = max_tokens or MAX_TOKENS
        
        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            elapsed_time = time.time() - start_time
            
            # Log usage information
            if hasattr(response, 'usage'):
                logger.info(
                    f"OpenAI API call: model={model}, "
                    f"prompt_tokens={response.usage.prompt_tokens}, "
                    f"completion_tokens={response.usage.completion_tokens}, "
                    f"total_tokens={response.usage.total_tokens}, "
                    f"time={elapsed_time:.2f}s"
                )
            
            return response
        
        except openai.RateLimitError as e:
            logger.warning(f"Rate limit exceeded: {str(e)}")
            raise
        except openai.APITimeoutError as e:
            logger.warning(f"API timeout: {str(e)}")
            raise
        except openai.APIConnectionError as e:
            logger.warning(f"API connection error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in OpenAI API call: {str(e)}")
            raise
    
    def count_tokens(self, text: str, model: Optional[str] = None) -> int:
        """
        Count the number of tokens in a text.
        
        Args:
            text: The text to count tokens for.
            model: The model to use for counting tokens.
            
        Returns:
            The number of tokens.
        """
        # This is a simplified implementation
        # For more accurate token counting, use tiktoken
        return len(text) // 4  # Rough approximation
    
    def chunk_text(self, text: str, max_chunk_tokens: int = 4000, model: Optional[str] = None) -> List[str]:
        """
        Split text into chunks that fit within token limits.
        
        Args:
            text: The text to split.
            max_chunk_tokens: Maximum tokens per chunk.
            model: The model to use for counting tokens.
            
        Returns:
            List of text chunks.
        """
        # This is a simplified implementation
        # For more sophisticated chunking, consider semantic chunking
        words = text.split()
        chunks = []
        current_chunk = []
        current_token_count = 0
        
        for word in words:
            word_token_count = self.count_tokens(word)
            if current_token_count + word_token_count > max_chunk_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_token_count = word_token_count
            else:
                current_chunk.append(word)
                current_token_count += word_token_count
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks

    def get_model_token_limit(self, model: Optional[str] = None) -> int:
        """
        Get the token limit for a specific model.
        
        Args:
            model: The model name.
            
        Returns:
            The token limit for the model.
        """
        model = model or self.model
        return MODEL_TOKEN_LIMITS.get(model, 4096)

# Create a default client instance
try:
    default_client = OpenAIClient()
except ValueError as e:
    logger.warning(f"Could not initialize default OpenAI client: {str(e)}")
    default_client = None

def get_client() -> OpenAIClient:
    """
    Get the default OpenAI client instance.
    
    Returns:
        The default OpenAI client.
    """
    if default_client is None:
        raise ValueError("Default OpenAI client is not initialized. Set OPENAI_API_KEY environment variable.")
    return default_client
