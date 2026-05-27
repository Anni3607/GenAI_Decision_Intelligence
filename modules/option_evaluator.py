import json
import re
import os

from groq import Groq

# =====================================================
# API CONFIG
# =====================================================

GROQ_API_KEY = "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"

client = Groq(
    api_key=GROQ_API_KEY
)

MODEL_NAME = "llama-3.3-70b-versatile"

# =====================================================
# AI OPTION EVALUATION
# =====================================================

def evaluate_options(
    domain,
    options,
    criteria
):

    prompt = f"""
You are an expert decision evaluation engine.

Domain:
{domain}

Options:
{options}

Criteria:
{criteria}

Task:
Evaluate EACH option on EACH criterion using a score from 1-10.

Rules:
- Return STRICT JSON only
- Scores must be realistic
- Be comparative and practical
- No explanations
- No markdown

Example format:

{{
  "Option A": {{
      "battery": 8,
      "camera": 7
  }},
  "Option B": {{
      "battery": 9,
      "camera": 8
  }}
}}
"""

    try:

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1200
        )

        response = completion.choices[0].message.content

        response = response.strip()

        json_match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL
        )

        if json_match:

            parsed = json.loads(
                json_match.group()
            )

            return parsed

        return {}

    except Exception as e:

        print(
            f"Evaluation Error: {str(e)}"
        )

        return {}
