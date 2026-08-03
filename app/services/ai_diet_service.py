import os
import json
import anthropic


class AIDietService:

    client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

    @staticmethod
    def build_prompt(report, daily_plan):

        analysis = report.analysis

        prompt = f"""
You are an experienced clinical nutritionist.

Patient Details

Health Score:
{analysis.health_score}

Risk Level:
{analysis.risk_level}

Abnormal Parameters:
{analysis.deficiencies}

Doctor Recommendations:
{analysis.recommendations}

Suggested Meal Plan:
{daily_plan}

Requirements:

1. Improve abnormal blood parameters.
2. Use Indian foods.
3. Keep meals practical.
4. Mention why each meal is useful.
5. Give hydration advice.
6. Mention foods to avoid.

Return ONLY JSON in this format:

{{
    "breakfast": {{
        "meal": "",
        "reason": ""
    }},
    "lunch": {{
        "meal": "",
        "reason": ""
    }},
    "snack": {{
        "meal": "",
        "reason": ""
    }},
    "dinner": {{
        "meal": "",
        "reason": ""
    }},
    "hydration": "",
    "avoid": []
}}
"""
        return prompt


    @staticmethod
    def generate(report, daily_plan):

        prompt = AIDietService.build_prompt(report, daily_plan)

        response = AIDietService.client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
        )

        text = None

        for block in response.content:
            # print("TYPE:", block.type)

            if block.type == "text":
               text = block.text
               break

        if text is None:
             raise Exception("Claude did not return a text response.")

        text = text.strip()

        if text.startswith("```json"):
           text = text[7:]

        if text.startswith("```"):
          text = text[3:]

        if text.endswith("```"):
           text = text[:-3]

        text = text.strip()

        return json.loads(text)