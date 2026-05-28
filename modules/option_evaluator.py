import json
import re

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
You are a highly realistic decision evaluation engine.

Your job is to evaluate options realistically,
critically,
and comparatively.

=====================================================

DOMAIN:
{domain}

OPTIONS:
{options}

CRITERIA:
{criteria}

=====================================================

IMPORTANT RULES:

1. Use scores from 1-10.

2. Be REALISTIC and GROUNDED.

3. Avoid giving high scores too easily.

4. Every option must have weaknesses.

5. Do NOT romanticize:
- entrepreneurship
- startups
- luxury products
- hype brands
- emotionally attractive lifestyles

6. Consider:
- hidden stress
- uncertainty
- sustainability
- long-term practicality
- real-world difficulty
- economic reality

7. Strong tradeoffs should exist naturally.

8. Use broader score distribution:
- average = 4-6
- strong = 7-8
- exceptional = 9
- very poor = 1-3

9. Avoid making all options similar.

10. Subjective criteria like:
- taste
- design
- style
- emotional_pull
- comfort

should vary significantly between options.

11. Career realism examples:
- owning a business usually has HIGH stress
- freelancing has income instability
- corporate jobs often reduce flexibility
- government jobs reduce risk but may reduce growth

12. Food realism examples:
- unhealthy foods may score high on taste
- healthy foods may score lower on emotional satisfaction
- fast food should not receive high healthiness

13. Investment realism examples:
- high returns usually imply higher risk
- stable investments rarely maximize growth

=====================================================

Return STRICT JSON ONLY.

NO explanations.
NO markdown.
NO extra text.

FORMAT:

{{
    "Option Name": {{
        "criterion": score
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
            temperature=0.2,
            max_tokens=1400
        )

        response = (
            completion
            .choices[0]
            .message
            .content
            .strip()
        )

        json_match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL
        )

        if json_match:

            parsed = json.loads(
                json_match.group()
            )

            # =========================================
            # SCORE NORMALIZATION
            # =========================================

            for option in parsed:

                for criterion in parsed[option]:

                    score = parsed[option][criterion]

                    # force valid range

                    if score < 1:
                        score = 1

                    if score > 10:
                        score = 10

                    parsed[option][criterion] = score

            return parsed

        return {}

    except Exception as e:

        print(
            f"Evaluation Error: {str(e)}"
        )

        return {}
