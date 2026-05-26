import os
import re
import json

from groq import Groq

# =====================================================
# API CONFIG
# =====================================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    "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"
)

client = Groq(
    api_key=GROQ_API_KEY
)

MODEL_NAME = "llama-3.3-70b-versatile"

# =====================================================
# CLEAN RESPONSE
# =====================================================

def clean_response(text):

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()

# =====================================================
# GENERIC AI REASONING
# =====================================================

def generate_reasoning(prompt):

    try:

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1200
        )

        response = completion.choices[0].message.content

        return clean_response(response)

    except Exception as e:

        return f"AI reasoning failed: {str(e)}"

# =====================================================
# EXTRACT DECISION CONTEXT
# =====================================================

def extract_decision_context(user_input):

    prompt = f"""
You are an intelligent decision analysis engine.

Extract the following from the user input:

1. Priorities
2. Concerns
3. Goals
4. Preferences
5. Constraints

Return STRICT JSON format only.

User Input:
{user_input}
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
            max_tokens=700
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

        return {
            "priorities": [],
            "concerns": [],
            "goals": [],
            "preferences": [],
            "constraints": []
        }

    except Exception as e:

        return {
            "error": str(e),
            "priorities": [],
            "concerns": [],
            "goals": [],
            "preferences": [],
            "constraints": []
        }
