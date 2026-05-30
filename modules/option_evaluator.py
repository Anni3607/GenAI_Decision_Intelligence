import json
import re
from groq import Groq
import streamlit as st

# =====================================================
# API CONFIG
# =====================================================

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    print("SECRET FOUND")
except Exception as e:
    print("SECRET ERROR:", str(e))
    GROQ_API_KEY = None

client = Groq(
    api_key=GROQ_API_KEY
)

MODEL_NAME = "llama-3.3-70b-versatile"

# =====================================================
# AI OPTION EVALUATION
# =====================================================

def evaluate_options(domain, options, criteria, user_input="", **kwargs):

    criteria_list = [
        c.lower().strip()
        for c in criteria
    ]

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
{criteria_list}

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

"I only care about salary"

→ salary should influence scoring heavily.

"I only care about health"

→ health-related criteria should dominate.

=====================================================

ANTI-BIAS RULES

Do NOT assume:

- startups are always better
- corporates are always better
- luxury is always better
- expensive means better
- famous brands always win

=====================================================

REALISM RULES

Most real-world scores should be:

1-3 = poor
4-6 = average
7-8 = strong
9 = exceptional
10 = extremely rare

Avoid unrealistic score gaps.

Strong options should still have weaknesses.

Weak options should still have strengths.

=====================================================

CAREER REALISM

- startups often increase uncertainty
- startups often increase stress
- freelancing increases income variability
- government jobs reduce risk
- large corporates usually improve stability

=====================================================

FOOD REALISM

- unhealthy foods can score high on taste
- healthy foods may score lower on cravings
- fast food should score lower on healthiness

=====================================================

TECH REALISM

- premium devices should lose on price
- budget devices can offer better value

=====================================================

FASHION REALISM

- luxury may improve style
- local products may improve value
- comfort does not always correlate with price

=====================================================

FITNESS REALISM

- effectiveness usually requires effort
- fast results often reduce sustainability

=====================================================

INVESTMENT REALISM

- higher returns usually imply higher risk
- stable investments rarely maximize growth

=====================================================

RETURN STRICT JSON ONLY.

CRITERION KEYS MUST MATCH EXACTLY:

{criteria_list}

FORMAT:

{{
    "Option Name": {{
        "criterion_name": score
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

        response = completion.choices[0].message.content

        if response is None:
            print("GROQ RETURNED NONE")
            return {}

        response = response.strip()

        print("========== RAW GROQ RESPONSE ==========")
        print(response)
        print("=======================================")

        if "```" in response:

            parts = response.split("```")

            if len(parts) >= 2:
                response = parts[1]

                if response.startswith("json"):
                    response = response[4:]

                response = response.strip()

        json_match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL
        )

        if not json_match:

            print("JSON MATCH FAILED")
            print(response)

            return {}

        parsed = json.loads(
            json_match.group()
        )

        cleaned_parsed = {}

        for option_name, scores in parsed.items():

            cleaned_scores = {}

            for criterion, score in scores.items():

                normalized_criterion = (
                    str(criterion)
                    .lower()
                    .strip()
                )

                try:
                    score_value = float(score)

                except Exception:
                    score_value = 5

                score_value = max(
                    1,
                    min(
                        10,
                        score_value
                    )
                )

                cleaned_scores[
                    normalized_criterion
                ] = round(score_value)

            for criterion in criteria_list:

                if criterion not in cleaned_scores:

                    cleaned_scores[
                        criterion
                    ] = 5

            cleaned_parsed[
                option_name
            ] = cleaned_scores

        print("========== CLEANED JSON ==========")
        print(cleaned_parsed)
        print("==================================")

        return cleaned_parsed

    except Exception as e:

        print("========== GROQ ERROR ==========")
        print(str(e))
        print("================================")

        st.sidebar.error(
            f"Groq API Call Error: {str(e)}"
        )

        return {}
