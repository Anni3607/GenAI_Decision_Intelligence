import os
import re

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
# GENERATE REASONING
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
