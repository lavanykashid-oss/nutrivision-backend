from dotenv import load_dotenv
import os
import anthropic

load_dotenv()

key = os.getenv("ANTHROPIC_API_KEY")

print("Key exists:", key is not None)
print("Starts with:", key[:15])

client = anthropic.Anthropic(
    api_key=key
)

print(client)

models = client.models.list()

for model in models.data:
    print(model.id)