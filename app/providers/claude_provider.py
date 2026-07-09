import os
from anthropic import Anthropic
import json
import base64
from PIL import Image
from io import BytesIO






class ClaudeProvider:

    def __init__(self):
        print("AI Provider:", os.getenv("AI_PROVIDER"))
       # print("Claude Key:", os.getenv("ANTHROPIC_API_KEY"))

        
        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def encode_image(self, image):

       image.seek(0)

       img = Image.open(image)

       if img.mode != "RGB":
           img = img.convert("RGB")

       img.thumbnail((512,512))

       buffer = BytesIO()

       img.save(
          buffer,
          format="JPEG",
          quality=75,
          optimize=True
       )

       image_bytes = buffer.getvalue()

       image.seek(0)

       return base64.b64encode(image_bytes).decode("utf-8")

    def generate_text(self, prompt):

        response = self.client.messages.create(

            model="claude-sonnet-5",

            max_tokens=1500,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )
        text_parts = []

        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            
        return "".join(text_parts).strip()
        

    def generate_json(self, prompt, image=None):

        if image:

          image_data = self.encode_image(image)

          response = self.client.messages.create(
            model="claude-sonnet-5",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content":[
                        {
                            "type":"image",
                            "source":{
                                "type":"base64",
                                "media_type":"image/jpeg",
                                "data":image_data
                            }
                        },
                        {
                            "type":"text",
                            "text":prompt
                        }
                    ]
                }
            ]
        )

        else:

           response = self.client.messages.create(
            model="claude-sonnet-5",
            max_tokens=2048,
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )


        

    
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        input_cost = (input_tokens / 1_000_000) * 3
        output_cost = (output_tokens / 1_000_000) * 15

        total_cost = input_cost + output_cost

        print("=" * 60)
        print("Claude Vision Usage")
        print("Input Tokens :", input_tokens)
        print("Output Tokens:", output_tokens)
        print(f"Estimated Cost: ${total_cost:.6f}")
        print("=" * 60)

        text = "".join(
          block.text
          for block in response.content
          if hasattr(block, "text")
        ).strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        return json.loads(text)

        

        