"""Debug script to check environment and config."""
import os
import sys

print("=" * 60)
print("ENVIRONMENT DEBUG")
print("=" * 60)

# Check if .env is loaded
print("\n1. Checking .env file:")
env_path = os.path.join(os.path.dirname(__file__), ".env")
print(f"   .env path: {env_path}")
print(f"   .env exists: {os.path.exists(env_path)}")

# Import config
print("\n2. Loading config...")
from config import settings

print(f"   LLM Provider: {settings.llm_provider}")
print(f"   Groq API Key: {settings.groq_api_key[:20]}..." if settings.groq_api_key else "   Groq API Key: None")
print(f"   OpenAI Model: {settings.openai_model}")

# Check environment variables
print("\n3. Environment variables:")
print(f"   GROQ_API_KEY: {os.environ.get('GROQ_API_KEY', 'NOT SET')[:20]}..." if os.environ.get('GROQ_API_KEY') else "   GROQ_API_KEY: NOT SET")
print(f"   OPENAI_API_KEY: {os.environ.get('OPENAI_API_KEY', 'NOT SET')}")
print(f"   GEMINI_API_KEY: {os.environ.get('GEMINI_API_KEY', 'NOT SET')}")

# Test agent config
print("\n4. Testing agent initialization:")
from agents.product_manager import ProductManagerAgent

agent = ProductManagerAgent()
print(f"   Agent Model: {agent.config.llm_model}")
print(f"   Agent Temperature: {agent.config.temperature}")

print("\n" + "=" * 60)
