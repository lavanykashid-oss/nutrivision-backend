import os
from google import genai
import json
from PIL import Image


class GeminiProvider:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def generate_text(self, prompt):

        response = self.client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        return response.text

    # def generate_json(self, prompt,image=None):

    def generate_json(self, prompt, image=None):

        if image:

            uploaded_image = Image.open(image)

            response = self.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=[
                   prompt,
                   uploaded_image
            ]
        )

        else:

           response = self.client.models.generate_content(
              model="gemini-2.5-flash-lite",
              contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```json"):
          text = text.replace("```json", "")
          text = text.replace("```", "").strip()

        return json.loads(text)

        
        