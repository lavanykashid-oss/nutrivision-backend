from app.providers.provider_factory import ProviderFactory


class AIService:

    @staticmethod
    def generate_text(prompt):

        provider = ProviderFactory.get_provider()

        return provider.generate_text(prompt)

    @staticmethod
    def generate_json(prompt, image=None):

        provider = ProviderFactory.get_provider()

        return provider.generate_json(
            prompt=prompt,
            image=image
        )