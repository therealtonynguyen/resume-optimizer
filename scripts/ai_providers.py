#!/usr/bin/env python3
"""
AI Provider abstraction layer for resume optimization.
Supports multiple AI providers including free options.
"""
import json
import re
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> str:
        """Generate a response from the AI provider.
        
        Args:
            system_prompt: System/instruction prompt
            user_prompt: User input prompt
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text response
        """
        pass


class OpenAIProvider(AIProvider):
    """OpenAI API provider (paid, but high quality)."""
    
    def __init__(self, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
    
    def generate(self, system_prompt: str, user_prompt: str, model: str = "gpt-4o", 
                 temperature: float = 0.7, max_tokens: int = 8000, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content


class OllamaProvider(AIProvider):
    """Ollama provider (FREE, local LLM - requires Ollama installed locally)."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.base_url = base_url
        self.model = model
        import requests
        self.requests = requests
    
    def generate(self, system_prompt: str, user_prompt: str, model: Optional[str] = None,
                 temperature: float = 0.7, max_tokens: int = 8000, **kwargs) -> str:
        model = model or self.model
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        response = self.requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            },
            timeout=300  # Ollama can be slow
        )
        response.raise_for_status()
        return response.json()["response"]


class GoogleGeminiProvider(AIProvider):
    """Google Gemini API provider (FREE tier available)."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        import requests
        self.requests = requests
    
    def generate(self, system_prompt: str, user_prompt: str, model: str = "gemini-pro",
                 temperature: float = 0.7, max_tokens: int = 8000, **kwargs) -> str:
        import time
        # Combine system and user prompts for Gemini
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        
        # Retry on rate limit (429) with exponential backoff
        max_retries = 3
        base_delay = 30  # seconds
        
        for attempt in range(max_retries + 1):
            response = self.requests.post(url, json=payload, timeout=120)
            
            if response.status_code == 429:
                if attempt < max_retries:
                    delay = base_delay * (2 ** attempt)
                    time.sleep(delay)
                    continue
                # Exhausted retries
                response.raise_for_status()
            
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]


class GroqProvider(AIProvider):
    """Groq API provider (FREE tier available, very fast)."""
    
    def __init__(self, api_key: str):
        from groq import Groq
        self.client = Groq(api_key=api_key)
    
    def generate(self, system_prompt: str, user_prompt: str, model: str = "llama-3.1-70b-versatile",
                 temperature: float = 0.7, max_tokens: int = 8000, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content


class HuggingFaceProvider(AIProvider):
    """Hugging Face Inference API provider (FREE tier available)."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        import requests
        self.requests = requests
    
    def generate(self, system_prompt: str, user_prompt: str, model: str = "mistralai/Mistral-7B-Instruct-v0.2",
                 temperature: float = 0.7, max_tokens: int = 8000, **kwargs) -> str:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        response = self.requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "inputs": full_prompt,
                "parameters": {
                    "temperature": temperature,
                    "max_new_tokens": min(max_tokens, 512)  # HF free tier limit
                }
            },
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "").replace(full_prompt, "").strip()
        return str(result)


def get_provider(provider_name: str, config: Dict[str, Any]) -> AIProvider:
    """Factory function to get the appropriate AI provider.
    
    Args:
        provider_name: Name of the provider ('openai', 'ollama', 'gemini', 'groq', 'huggingface')
        config: Configuration dictionary with API keys and settings
        
    Returns:
        AIProvider instance
    """
    provider_name = provider_name.lower()
    
    if provider_name == "openai":
        api_key = config.get('openai_api_key')
        if not api_key:
            raise ValueError("openai_api_key not found in config")
        return OpenAIProvider(api_key)
    
    elif provider_name == "ollama":
        base_url = config.get('ollama_base_url', 'http://localhost:11434')
        model = config.get('ollama_model', 'llama3.2')
        return OllamaProvider(base_url=base_url, model=model)
    
    elif provider_name == "gemini":
        api_key = config.get('gemini_api_key')
        if not api_key:
            raise ValueError("gemini_api_key not found in config")
        return GoogleGeminiProvider(api_key)
    
    elif provider_name == "groq":
        api_key = config.get('groq_api_key')
        if not api_key:
            raise ValueError("groq_api_key not found in config")
        return GroqProvider(api_key)
    
    elif provider_name == "huggingface":
        api_key = config.get('huggingface_api_key')
        if not api_key:
            raise ValueError("huggingface_api_key not found in config")
        return HuggingFaceProvider(api_key)
    
    else:
        raise ValueError(f"Unknown provider: {provider_name}. Supported: openai, ollama, gemini, groq, huggingface")
