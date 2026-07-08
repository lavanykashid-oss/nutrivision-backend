import os

from app.providers.gemini_provider import GeminiProvider
from app.providers.claude_provider import ClaudeProvider


class ProviderFactory:

    @staticmethod
    def get_provider():

        provider = os.getenv("AI_PROVIDER", "gemini").lower()

        print("current key provider:", provider)

        if provider == "claude":
            return ClaudeProvider()

        return GeminiProvider()