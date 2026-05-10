"""Provider initialization and registration"""

from app.config import settings
from app.providers.registry import register_provider
from app.providers.openai import OpenAIProvider
from app.providers.anthropic import AnthropicProvider
from app.providers.groq import GroqProvider
from app.providers.openrouter import OpenRouterProvider
from app.providers.mistral import MistralProvider
from app.providers.google import GoogleProvider
from app.providers.nvidia import NVIDIAProvider


def init_providers():
    """Initialize and register all available providers."""
    
    # OpenAI (paid, but most popular)
    if settings.openai_api_key:
        register_provider("openai", OpenAIProvider(settings.openai_api_key))
    
    # Anthropic (paid)
    if settings.anthropic_api_key:
        register_provider("anthropic", AnthropicProvider(settings.anthropic_api_key))
    
    # Groq (free tier available)
    if settings.groq_api_key:
        register_provider("groq", GroqProvider(settings.groq_api_key))
    
    # OpenRouter (free tier + paid models)
    if settings.openrouter_api_key:
        register_provider("openrouter", OpenRouterProvider(settings.openrouter_api_key))
    
    # Mistral (paid, but affordable)
    if settings.mistral_api_key:
        register_provider("mistral", MistralProvider(settings.mistral_api_key))
    
    # Google Gemini (free tier available)
    if settings.google_api_key:
        register_provider("google", GoogleProvider(settings.google_api_key))
    
    # NVIDIA NIM (free tier available)
    if settings.nvidia_api_key:
        register_provider("nvidia", NVIDIAProvider(settings.nvidia_api_key))
