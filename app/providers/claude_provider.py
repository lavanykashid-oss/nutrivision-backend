import os
import json
import base64
import re

from anthropic import Anthropic
from PIL import Image
from io import BytesIO

try:
    import resource
except ImportError:
    resource = None


class ClaudeProvider:

    # ============================================================
    # MEMORY LOGGER
    # ============================================================

    def log_memory(self, label):

        try:
            current_mb = None
            peak_mb = None
            cgroup_mb = None
            limit_mb = None

        # Current + peak process RSS
            with open("/proc/self/status", "r") as f:
                for line in f:

                    if line.startswith("VmRSS:"):
                        current_mb = int(line.split()[1]) / 1024
 
                    elif line.startswith("VmHWM:"):
                       peak_mb = int(line.split()[1]) / 1024

        # Render/container current memory
            try:
                with open("/sys/fs/cgroup/memory.current", "r") as f:
                    cgroup_mb = int(f.read().strip()) / 1024 / 1024
            except Exception:
                pass

        # Render/container memory limit
            try:
                with open("/sys/fs/cgroup/memory.max", "r") as f:
                    value = f.read().strip()

                    if value != "max":
                       limit_mb = int(value) / 1024 / 1024
            except Exception:
                pass

            print(
            f"[MEMORY] {label} | "
            f"RSS={current_mb:.2f} MB | "
            f"PEAK={peak_mb:.2f} MB | "
            f"CGROUP={cgroup_mb:.2f} MB | "
            f"LIMIT={limit_mb:.2f} MB",
            flush=True
        )

        except Exception as e:

         print(
            f"[MEMORY] {label} | unable to read memory: {e}",
            flush=True
        )
    # ============================================================
    # INITIALIZE PROVIDER
    # ============================================================

    def __init__(self):

        print(
            "AI Provider:",
            os.getenv("AI_PROVIDER")
        )

        # Keep this client because generate_text() uses it.
        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    # ============================================================
    # ENCODE IMAGE
    # ============================================================

    def encode_image(self, image):

        image.seek(0)

        img = Image.open(image)

        if img.mode != "RGB":
            img = img.convert("RGB")

        # Resize image to reduce token usage.
        img.thumbnail(
            (1024, 1024)
        )

        buffer = BytesIO()

        img.save(
            buffer,
            format="JPEG",
            quality=80,
            optimize=True
        )

        image_bytes = (
            buffer.getvalue()
        )

        image.seek(0)

        return base64.b64encode(
            image_bytes
        ).decode("utf-8")

    # ============================================================
    # GENERATE TEXT
    # ============================================================

    def generate_text(self, prompt):

        try:

            response = (
                self.client.messages.create(
                    model="claude-sonnet-5",
                    max_tokens=4096,
                    temperature=0,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
            )

            text_parts = []

            for block in response.content:

                if hasattr(
                    block,
                    "text"
                ):

                    text_parts.append(
                        block.text
                    )

            text = "".join(
                text_parts
            ).strip()

            return text

        except Exception as e:

            print("=" * 60)
            print(
                "CLAUDE TEXT API ERROR"
            )
            print("=" * 60)

            print(
                type(e).__name__,
                str(e)
            )

            print("=" * 60)

            return None

    # ============================================================
    # GENERATE JSON
    # ============================================================

    def generate_json(
        self,
        prompt,
        image=None
    ):

        client = None

        try:

            # ====================================================
            # BUILD MESSAGE
            # ====================================================

            if image:

                print(
                    "Claude Vision: "
                    "Processing image..."
                )

                image_data = (
                    self.encode_image(
                        image
                    )
                )

                content = [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type":
                                "image/jpeg",
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]

            else:

                content = [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]

            # ====================================================
            # CLAUDE API REQUEST
            # ====================================================

            print(
                "Sending request "
                "to Claude..."
            )

            # Create a temporary client for this JSON call.
            client = Anthropic(
                api_key=os.getenv(
                    "ANTHROPIC_API_KEY"
                )
            )

            self.log_memory(
                "before Claude call"
            )

            response = (
                client.messages.create(
                    model="claude-sonnet-5",
                    max_tokens=1024,
                    messages=[
                        {
                            "role": "user",
                            "content": content
                        }
                    ]
                )
            )

            self.log_memory(
                "after Claude call"
            )

            # ====================================================
            # TOKEN USAGE
            # ====================================================

            input_tokens = (
                response.usage.input_tokens
            )

            output_tokens = (
                response.usage.output_tokens
            )

            input_cost = (
                input_tokens
                / 1_000_000
            ) * 3

            output_cost = (
                output_tokens
                / 1_000_000
            ) * 15

            total_cost = (
                input_cost
                + output_cost
            )

            print("=" * 60)
            print("Claude Usage")
            print(
                "Input Tokens :",
                input_tokens
            )
            print(
                "Output Tokens:",
                output_tokens
            )

            print(
                f"Estimated Cost: "
                f"${total_cost:.6f}"
            )

            print("=" * 60)

            # ====================================================
            # EXTRACT TEXT FROM RESPONSE
            # ====================================================

            text_parts = []

            for block in response.content:

                if hasattr(
                    block,
                    "text"
                ):

                    text_parts.append(
                        block.text
                    )

            text = "".join(
                text_parts
            ).strip()

            # ====================================================
            # DEBUG RAW RESPONSE
            # ====================================================

            print("=" * 60)
            print(
                "RAW CLAUDE RESPONSE"
            )
            print("=" * 60)

            print(
                repr(text)
            )

            print("=" * 60)

            # ====================================================
            # CHECK EMPTY RESPONSE
            # ====================================================

            if not text:

                print(
                    "ERROR: Claude returned "
                    "EMPTY response"
                )

                return None

            # ====================================================
            # REMOVE MARKDOWN CODE BLOCK
            # ====================================================

            text = text.strip()

            if text.startswith(
                "```json"
            ):

                text = text[
                    len("```json"):
                ].strip()

            elif text.startswith(
                "```"
            ):

                text = text[
                    len("```"):
                ].strip()

            if text.endswith(
                "```"
            ):

                text = text[
                    :-3
                ].strip()

            # ====================================================
            # FIND JSON OBJECT
            # ====================================================

            start = text.find("{")
            end = text.rfind("}")

            if (
                start == -1
                or end == -1
            ):

                print(
                    "ERROR: No JSON "
                    "object found in "
                    "Claude response"
                )

                print(
                    "Claude returned:"
                )

                print(text)

                return None

            json_text = text[
                start:end + 1
            ]

            # ====================================================
            # PARSE JSON
            # ====================================================

            try:

                result = json.loads(
                    json_text
                )

            except json.JSONDecodeError as e:

                print("=" * 60)
                print(
                    "CLAUDE JSON "
                    "PARSE ERROR"
                )
                print("=" * 60)

                print(
                    "Error:",
                    e
                )

                print(
                    "JSON TEXT:"
                )

                print(
                    json_text
                )

                print("=" * 60)

                return None

            # ====================================================
            # VALIDATE RESULT
            # ====================================================

            if not isinstance(
                result,
                dict
            ):

                print(
                    "ERROR: Claude JSON "
                    "is not an object"
                )

                return None

            # ====================================================
            # SUCCESS
            # ====================================================

            print("=" * 60)

            print(
                "Claude JSON parsed "
                "successfully"
            )

            print(
                "JSON keys:",
                list(
                    result.keys()
                )
            )

            print("=" * 60)

            return result

        # ========================================================
        # GENERAL API ERROR
        # ========================================================

        except Exception as e:

            print("=" * 60)
            print(
                "CLAUDE API ERROR"
            )
            print("=" * 60)

            print(
                "Error Type:",
                type(e).__name__
            )

            print(
                "Error:",
                str(e)
            )

            print("=" * 60)

            return None

        # ========================================================
        # CLEANUP TEMPORARY CLIENT
        # ========================================================

        finally:

            if client is not None:

                try:

                    client.close()

                    self.log_memory(
                        "after client close"
                    )

                except Exception as e:

                    print(
                        "Claude client close "
                        "warning:",
                        str(e)
                    )