
from groq import Groq
import os
import json
import re

client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)

MODEL_NAME = "llama-3.3-70b-versatile"


# ==========================================
# CLEAN JSON
# ==========================================

def clean_json_response(text):

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    return text.strip()


# ==========================================
# ADVANCED DECISION EXTRACTION
# ==========================================

def extract_decision_context(user_input):

    system_prompt = """
You are an advanced AI decision intelligence engine.

Your task:
Analyze the user's decision-making psychology.

Detect:

1. explicit priorities
2. hidden priorities
3. emotional concerns
4. risk tolerance
5. burnout sensitivity
6. conflict patterns
7. stability preferences
8. decision type

IMPORTANT:
Return ONLY valid JSON.

NO markdown.
NO explanations.
NO code fences.

Required JSON structure:

{
    "priorities": {},
    "hidden_priorities": [],
    "concerns": [],
    "goals": [],
    "risk_tolerance": "",
    "burnout_sensitivity": "",
    "decision_conflicts": [],
    "decision_type": ""
}
"""

    response = client.chat.completions.create(

        messages=[

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": user_input
            }

        ],

        model=MODEL_NAME,
        temperature=0.2
    )

    content = response.choices[0].message.content

    cleaned_content = clean_json_response(content)

    try:

        parsed = json.loads(cleaned_content)

        return parsed

    except Exception as e:

        return {
            "error": "Invalid JSON returned",
            "exception": str(e),
            "raw_output": cleaned_content
        }


# ==========================================
# AI REASONING
# ==========================================

def generate_reasoning(summary_prompt):

    response = client.chat.completions.create(

        messages=[

            {
                "role": "user",
                "content": summary_prompt
            }

        ],

        model=MODEL_NAME,
        temperature=0.4
    )

    return response.choices[0].message.content
