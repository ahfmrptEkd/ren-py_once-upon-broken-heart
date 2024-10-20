__version__ = "1.0.0"

# Import required libraries
import requests
import json
import time
import os

from .chatgpt_handler import ChatGPTHandler

# Define the completion function that takes messages and an API key as input
def completion(messages, api_key="", proxy=''):
    assistant_id = "asst_OHckidA2O7Ate1h3ctuKKZKQ"  # api assistant id
    base_url = proxy if proxy else "https://api.openai.com/v1"
    
    handler = ChatGPTHandler(api_key, assistant_id, base_url)
    return handler.completion(messages)
