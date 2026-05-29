import json
import re

from groq import Groq
import streamlit as st

# =====================================================
# API CONFIG
# =====================================================

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

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
    criteria,
    user_input=""
):

    prompt = f"""
You are a realistic decision intelligence engine.

Your job is to evaluate options realistically,
comparatively,
and according to the user's priorities.

=====================================================

DOMAIN:
{domain}

USER PRIORITIES:
{user_input}

OPTIONS:
{options}

CRITERIA:
{criteria}

=====================================================

IMPORTANT RULES

1. Use scores from 1-10.

2. Compare options AGAINST EACH OTHER.

3. Do NOT evaluate options independently.

4. Every option must have strengths.

5. Every option must have weaknesses.

6. User priorities matter.

If the user explicitly states a goal,
that goal should strongly influence evaluation.

Examples:

If the user says:
"I only care about salary"

then salary differences should be emphasized.

If the user says:
"I only care about health"

then health-related criteria should be emphasized.

If the user says:
"I want something cheap"

then affordability should be emphasized.

=====================================================

ANTI-BIAS RULES

Do NOT assume:

- startups are always better for growth
- corporates are always better for salary
- luxury products are always superior
- expensive automatically means better
- premium brands always win

=====================================================

SCORING GUIDELINES

1-3 = poor

4-6 = average

7-8 = strong

9 = exceptional

10 = extremely rare

Most real-world options should score
between 4 and 8.

=====================================================

COMPARISON RULES

Do NOT rank every criterion
in the same order.

Bad Example:

Google:
salary=9
growth=9
learning=9

Amazon:
salary=8
growth=8
learning=8

Microsoft:
salary=7
growth=7
learning=7

Good Example:

Google:
salary=9
growth=8
learning=8

Amazon:
salary=8
growth=9
learning=9

Microsoft:
salary=8
growth=7
learning=8

=====================================================

REALISM RULES

If two options are reasonably comparable,
their scores should differ by only 1-3 points.

Avoid unrealistic score gaps.

Strong options should still have weaknesses.

Weak options should still have strengths.

=====================================================

CAREER REALISM

- startups usually increase uncertainty
- startups often increase stress
- freelancing introduces income variability
- government jobs reduce risk
- large corporates usually offer stability
- salary depends on role, not stereotypes

=====================================================

FOOD REALISM

- unhealthy foods can score high on taste
- healthy foods may score lower on cravings
- fast food should score lower on healthiness
- expensive food is not automatically healthier

=====================================================

TECH REALISM

- expensive devices should lose on price
- budget devices can provide strong value
- premium devices should not dominate every criterion

=====================================================

FASHION REALISM

- luxury products may score higher on style
- local products often provide better value
- comfort does not always correlate with price
- trendiness and durability can conflict

=====================================================

FITNESS REALISM

- effective methods usually require effort
- low effort rarely produces exceptional outcomes
- sustainability matters

=====================================================

INVESTMENT REALISM

- higher returns usually imply higher risk
- stable investments rarely maximize growth
- liquidity and growth often trade off

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
            temperature=0.15,
            max_tokens=1500
        )

        response = (
            completion
            .choices[0]
            .message
            .content
            .strip()
        )

        json_match = re.search(
            r"\{{.*\}}",
            response,
            re.DOTALL
        )

        if json_match:

            parsed = json.loads(
                json_match.group()
            )

            for option in parsed:

                for criterion in parsed[option]:

                    score = parsed[option][criterion]

                    try:
                        score = float(score)
                    except:
                        score = 5

                    score = max(
                        1,
                        min(
                            10,
                            score
                        )
                    )

                    parsed[option][criterion] = round(score)

            return parsed

        return {}

    except Exception as e:

        print(
            f"Evaluation Error: {str(e)}"
        )

        return {}
